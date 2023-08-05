"""
 * Copyright (C) 2021 - Andrea Tangherloni
 * Distributed under the terms of the GNU General Public License (GPL)
 * This file is part of scAEspy.

 * scAEspy is a free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License v3.0 as published by
 * the Free Software Foundation.
  
 * scAEspy is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
"""

import warnings
warnings.simplefilter(action='ignore')

import os, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
if type(tf.contrib) != type(tf): tf.contrib._warning = None

import random
import numpy as np
import matplotlib as mpl
mpl.use('Agg')

from matplotlib import pylab as plt
import seaborn as sns

from tensorflow.contrib.layers import xavier_initializer
slim = tf.contrib.slim

from _version import __version__

# Core class of scAEspy
class scAEspy(object):

	def __init__(self,
				 original_dim,
				 hidden_layers=[128],
				 latent_layer=32,
				 activation='sigmoid',
				 rec_loss='Poisson',
				 num_gaussians=1,
				 learnable_prior=True,
				 alpha=0,
				 lambd=2,
				 constrained=False,
				 clipping=False,
				 verbose=False,
				 seed=None):

		self.__original_dim    = original_dim       # The number of genes of the gene expression matrix 
		self.__hidden_layers   = hidden_layers      # List of the dimensions of the hidden layers
		self.__latent_layer    = latent_layer       # The dimension of the latent space
		self.__rec_loss        = rec_loss           # The desidered loss function (i.e., Poisson, ZIP, NB, ZINB, MSE)
		self.__num_gaussians   = num_gaussians      # The desidered number of Gaussian distribution(s)
		self.__learnable_prior = learnable_prior    # Whether the prior distribution in the latent space has to be learnt or not
		self.__alpha           = alpha
		self.__lambda          = lambd
		self.__constrained     = constrained        # Whether the loss function has to be constrained or not
		self.__clipping        = clipping           # Enable or disable the clipping modality to avoid as much as possible NaNs
		self.__verbose         = verbose            # Enable or disable the verbose modality
		self.__seed            = seed               # The desidered seed
		self.__epoch           = 0                  # The number of epochs
		self.__zerosCells      = None

		# Check the MSE loss function (a constrained version of MSE is not supported yet)
		if self.__constrained and self.__rec_loss =="MSE":
			print("* Warning, a constrained version of MSE is not supported. constrained sets to False")
			self.__constrained = False

		# Check the required loss function (we provide the following loss functions: Poisson, ZIP, NB, ZINB, and MSE)
		if self.__rec_loss not in ["Poisson", "ZIP", "NB", "ZINB", "MSE"]:
			print("* %s is not supported. The provided loss functions are: Poisson, ZIP, NB, ZINB, and MSE"%self.__rec_loss)
			exit(-1)

		# Check the required activation function (It can be any callable activation function)
		if activation =="relu":
			self.__activation = tf.nn.relu
		elif activation=="sigmoid":
			self.__activation = tf.nn.sigmoid
		elif activation is None:
			self.__activation = None
		elif callable(activation):
			self.__activation = activation
		else:
			print("* %s is not supported. You can use 'sigmoid', 'relu', None, and all tensorflow activation functions"%activation)
			exit(-2)

		# Enable the verbose modality
		if self.__verbose:
			print("* Using %d hidden layers"%len(self.__hidden_layers), self.__hidden_layers)
			print("* Latent space: %d dimensions"%self.__latent_layer)
			print("* Using %s as activation function"%self.__activation)
			
		# Create the history structure to store the all the components of the ELBO function
		self.__sess_info       = None
		self.__history = {
			'test_kly':[],
			'test_rec':[],
			'test_klz':[],
			'test_mmd':[],
			'test_loss':[],
			'train_kly':[],
			'train_rec':[],
			'train_klz':[],
			'train_mmd':[],
			'train_loss':[]
		}


		# Set the seed for reproducibility, if required.
		if self.__seed is not None:

			if self.__verbose:
				print("* Setting seed to %d for reproducibility" % self.__seed)

			random.seed(self.__seed)
			np.random.seed(self.__seed)
			tf.set_random_seed(self.__seed)
			os.environ['PYTHONHASHSEED'] = str(self.__seed)

	# Definition of the MSE loss function
	def __MSE(self, x, logits, axis=-1):
		return tf.reduce_sum(tf.square(x-logits), axis)

	# Definition of the Poisson loss function
	def __log_poisson_with_logits(self, x, x_logits, axis=-1):
		return tf.reduce_sum(tf.nn.log_poisson_loss(log_input=x_logits, targets=x), axis)

	# Definition of the zero-inflated Poisson loss function
	def __log_zero_inflated_poisson_with_logits(self, x, x_logits, p_logits, axis=-1):
		
		# For numerical stability, we added a epsilon term
		eps = 1e-10
		nb_case = tf.nn.log_poisson_loss(log_input=x_logits, targets=x) - tf.log(1.0-p_logits+eps)

		x_logits  = tf.exp(x_logits)
		p_logits  = tf.nn.sigmoid(p_logits)
		
		zero_p    = tf.exp(-x_logits)
		zero_case = tf.log(p_logits + ((1.0-p_logits)*zero_p)+eps)
		result    = tf.where(tf.less(x, 1e-8), zero_case, nb_case)
		
		return tf.reduce_sum(result, axis)

	# Base function for the NB loss functions
	def __log_negative_binomial(self, x, x_logits, s_logits):
		
		# For numerical stability, we added a epsilon term
		eps = 1e-10
		t1 = tf.lgamma(s_logits+eps) + tf.lgamma(x+1.0) - tf.lgamma(x+s_logits+eps)
		t2 = (s_logits+x) * tf.log(1.0 + (x_logits/(s_logits+eps))) + (x * (tf.log(s_logits+eps) - tf.log(x_logits+eps)))

		return t1+t2

	# Definition of the NB loss function
	def __log_negative_binomial_with_logits(self, x, x_logits, s_logits, axis=-1):

		# Clip the values to avoid NaNs
		if self.__clipping:
			x_logits = tf.clip_by_value(tf.exp(x_logit), 1e-3, 1e3)
			s_logits = tf.clip_by_value(tf.nn.softplus(s_logit), 1e-3, 1e3)

		else:
			x_logits = tf.exp(x_logits)
			s_logits = tf.nn.softplus(s_logits)   

		return tf.reduce_sum(self.__log_negative_binomial(x, x_logits, s_logits), axis)

	# Definition of the zero-inflated NB loss function
	def __log_zero_inflated_negative_binomial_with_logits(self, x, x_logits, s_logits, p_logits, axis=-1):

		# Clip the values to avoid NaNs
		if self.__clipping:
			x_logit = tf.clip_by_value(tf.exp(x_logit), 1e-3, 1e3)
			s_logit = tf.clip_by_value(tf.nn.softplus(s_logit), 1e-3, 1e3)
		
		else:
			x_logits = tf.exp(x_logits)
			s_logits = tf.nn.softplus(s_logits)
		
		p_logits = tf.nn.sigmoid(p_logits)

		eps = 1e-10
		nb_case = self.__log_negative_binomial(x, x_logits, s_logits) - tf.log(1.0-p_logits+eps)

		zero_nb   = tf.pow(s_logits/(s_logits+x_logits+eps), s_logits)
		zero_case = tf.log(p_logits + ((1.0-p_logits)*zero_nb)+eps)
		result    = tf.where(tf.less(x, 1e-8), zero_case, nb_case)
		
		return tf.reduce_sum(result, axis)

	# Log transformation of a Normal distribution 
	def __log_normal(self, x, mu, var, axis=-1):
		return -0.5 * tf.reduce_sum(tf.log(2 * np.pi) + tf.log(var) + tf.square(x - mu) / var, axis)
	
	# Function that computes the Gaussian kernel for the MMD divergence function
	def __compute_kernel(self, x, y):

		x_size  = tf.shape(x)[0]
		y_size  = tf.shape(y)[0]

		dim     = tf.shape(x)[1]

		tiled_x = tf.tile(tf.reshape(x, tf.stack([x_size, 1, dim])), tf.stack([1, y_size, 1]))
		tiled_y = tf.tile(tf.reshape(y, tf.stack([1, y_size, dim])), tf.stack([x_size, 1, 1]))

		return tf.exp(-tf.reduce_sum(tf.square(tiled_x - tiled_y), axis=2)/ tf.cast(dim, tf.float32))        

	# Definition of the prior on the latent space (y variable)
	def __prior_y_logit(self, y):

		with slim.arg_scope([slim.fully_connected],
							activation_fn=tf.nn.relu,
							weights_initializer=xavier_initializer(),
							biases_initializer=tf.zeros_initializer(),
							reuse=tf.AUTO_REUSE):
			
			# Learnable distribution of the categorical variable y
			if self.__learnable_prior:
				y_prior_logit = slim.fully_connected(y, 1, activation_fn=None, scope='y_prior1')
			
			# Uniform distribution of the categorical variable y
			else:
				y_prior_logit = slim.fully_connected(y, 1, activation_fn=None, weights_initializer=tf.zeros_initializer(), biases_initializer=tf.zeros_initializer(), trainable=False, scope='y_prior1')
				
			return y_prior_logit  

	def __qy_graph(self, x, k):

		with slim.arg_scope([slim.fully_connected],
							activation_fn=tf.nn.sigmoid,
							weights_initializer=xavier_initializer(),
							biases_initializer=tf.zeros_initializer(),
							reuse=tf.AUTO_REUSE):
			
			qy_logit = x
			for idx,hidden in enumerate(self.__hidden_layers):
				qy_logit = slim.fully_connected(qy_logit, hidden, scope='qy_graph%d'%idx, activation_fn=self.__activation)


			qy_logit = slim.fully_connected(qy_logit, k, activation_fn=None, scope='logit')
			qy = tf.nn.softmax(qy_logit, name='prob')

			return qy_logit, qy

	def __qz_graph(self, x, y):

		with slim.arg_scope([slim.fully_connected],
							activation_fn=tf.nn.sigmoid,
							weights_initializer=xavier_initializer(),
							biases_initializer=tf.zeros_initializer(),
							reuse=tf.AUTO_REUSE):



			mu_logvar = tf.concat([x, y], 1, name='xy/concat')
			
			for idx,hidden in enumerate(self.__hidden_layers):
				mu_logvar = slim.fully_connected(mu_logvar, hidden, scope='qz_graph%d'%idx, activation_fn=self.__activation)

			mu_logvar = slim.fully_connected(mu_logvar, 2*self.__latent_layer, activation_fn=None, scope='mu_logvar')

			mu, logvar = tf.split(mu_logvar, num_or_size_splits=2, axis=1)
			stddev     = tf.sqrt(tf.exp(logvar))

			# Draw a z from the distribution
			epsilon = tf.random_normal(tf.shape(stddev))
			z = mu + tf.multiply(stddev, epsilon)

			return z, mu, logvar
	
	def __prior_z(self, y):

		with slim.arg_scope([slim.fully_connected],
							activation_fn=tf.nn.sigmoid,
							weights_initializer=xavier_initializer(),
							biases_initializer=tf.zeros_initializer(),
							reuse=tf.AUTO_REUSE): 

			# ---p(z)
			mu_logvar = slim.fully_connected(y, 2*self.__latent_layer, activation_fn=None, scope='prior_z')
			mu, logvar = tf.split(mu_logvar, num_or_size_splits=2, axis=1)

			return mu, logvar

	# Internal function to select the desidered loss function
	def __labeled_loss(self, x, z, zm, zv, zm_prior, zv_prior, px_logit, ps_logit=None, pp_logit=None):

		if self.__rec_loss=="Poisson":
			loss  = self.__log_poisson_with_logits(x, px_logit)
		
		elif self.__rec_loss=="MSE":
			loss  = self.__MSE(x, px_logit)

		elif self.__rec_loss=="ZIP":
			loss  = self.__log_zero_inflated_poisson_with_logits(x, px_logit, pp_logit)

		elif self.__rec_loss=="NB":
			loss  = self.__log_negative_binomial_with_logits(x, px_logit, ps_logit)

		elif self.__rec_loss=="ZINB":
			loss  = self.__log_zero_inflated_negative_binomial_with_logits(x, px_logit, ps_logit, pp_logit)

		# Approximation of the KL divergence function
		apKLz = self.__log_normal(z, zm, zv) - self.__log_normal(z, zm_prior, zv_prior)

		return loss, apKLz

	# Maximum Mean Discrepancy divergence function
	def __MMD(self, qy, z_prior, z, batch_size):

		mmd = [None] * self.__num_gaussians

		for i in range(self.__num_gaussians):
			mmd[i] = 0
			x = z_prior[i]

			for j in range(self.__num_gaussians):
				y = z[j] #from the posterior distribution

				x_kernel  = self.__compute_kernel(x, x)
				y_kernel  = self.__compute_kernel(y, y)
				xy_kernel = self.__compute_kernel(x, y)

				e1       = tf.tensordot(qy[:,i], qy[:,j], axes=0)
				y_kernel = y_kernel*e1
				y_kernel = tf.reduce_mean(y_kernel)

				e1       = tf.tensordot(tf.ones([1, batch_size], tf.float32)/tf.cast(self.__num_gaussians,tf.float32), tf.ones([1, batch_size], tf.float32)/tf.cast(self.__num_gaussians, tf.float32), axes=0)
				x_kernel = x_kernel*e1
				x_kernel = tf.reduce_mean(x_kernel)

				e1        = tf.tensordot(tf.ones([1, batch_size], tf.float32)/tf.cast(self.__num_gaussians,tf.float32), qy[:,j], axes=0)
				xy_kernel = xy_kernel*e1
				xy_kernel = tf.reduce_mean(xy_kernel)

				v       = x_kernel + y_kernel - 2 * xy_kernel
				mmd[i] += v

		mmdMean = tf.reduce_sum(mmd)

		return mmdMean

	# Decoder Neural Network
	def __decoder(self, z, y):
		with slim.arg_scope([slim.fully_connected],
							activation_fn=tf.nn.sigmoid,
							weights_initializer=xavier_initializer(),
							biases_initializer=tf.zeros_initializer(),
							reuse=tf.AUTO_REUSE): 

			# ---p(z)
			mu, logvar = self.__prior_z(y)

			# ---p(x)
			logit = z
			for idx,hidden in enumerate(self.__hidden_layers):
				logit = slim.fully_connected(logit, hidden, scope='p_x%d'%idx, activation_fn=self.__activation)

			x_logit = slim.fully_connected(logit, self.__original_dim , activation_fn=None, scope='x_logit')
			
			if self.__rec_loss == "NB":
				s_logit = slim.fully_connected(logit, self.__original_dim , activation_fn=None, scope='s_logit')
				return mu, logvar, x_logit, s_logit

			if self.__rec_loss == "ZINB":
				s_logit = slim.fully_connected(logit, self.__original_dim , activation_fn=None, scope='s_logit')
				p_logit = slim.fully_connected(logit, self.__original_dim , activation_fn=None, scope='p_logit')

				return mu, logvar, x_logit, s_logit, p_logit

			if self.__rec_loss == "ZIP":
				p_logit = slim.fully_connected(logit, self.__original_dim , activation_fn=None, scope='p_logit')

				return mu, logvar, x_logit, p_logit

			else:

				return mu, logvar, x_logit

	# Build the whole AE (i.e., encoder, decoder, loss function and divergence functions)
	def __build(self):

		tf.reset_default_graph()

		# Reset the seed for reproducibility, if required. 
		if self.__seed is not None:
			random.seed(self.__seed)
			np.random.seed(self.__seed)
			tf.set_random_seed(self.__seed)
			os.environ['PYTHONHASHSEED'] = str(self.__seed)

		x_input   = tf.placeholder(tf.float32,[None, self.__original_dim ], name='x')
		x_output  = tf.placeholder(tf.float32,[None, self.__original_dim ], name='x_output')

		x_input_cast  = tf.cast(x_input, tf.float32)
		x_output_cast = tf.cast(x_output, tf.float32)

		batch_size = tf.shape(x_input_cast)[0]

		y_           = tf.fill(tf.stack([tf.shape(x_input_cast)[0], self.__num_gaussians]), 0.0)
		qy_logit, qy = self.__qy_graph(x_input_cast, self.__num_gaussians)

		y_prior_logit_lst = []

		z, zm, zv, zm_prior, zv_prior, px_logit, ps_logit, pp_logit = [[None] * self.__num_gaussians for i in range(8)]

		# Cycling over the desidered number of Gaussian distribution(s)
		for i in range(self.__num_gaussians):
			with tf.name_scope('graphs/hot_at{:d}'.format(i)):
				y = tf.add(y_, tf.constant(np.eye(self.__num_gaussians)[i], dtype=tf.float32, name='hot_at_{:d}'.format(i)))

				z[i], zm[i], zv[i] = self.__qz_graph(x_input_cast, y)

				# Different loss functions require different parameters
				if self.__rec_loss == "NB":
					zm_prior[i], zv_prior[i], px_logit[i], ps_logit[i] = self.__decoder(z[i], y)
				elif self.__rec_loss == "ZINB":
					zm_prior[i], zv_prior[i], px_logit[i], ps_logit[i], pp_logit[i] = self.__decoder(z[i], y)
				elif self.__rec_loss == "ZIP":
					zm_prior[i], zv_prior[i], px_logit[i], pp_logit[i] = self.__decoder(z[i], y)
				else:
					zm_prior[i], zv_prior[i], px_logit[i] = self.__decoder(z[i], y)
				
				y_prior_logit_lst.append(self.__prior_y_logit(y))
				
				if self.__constrained and self.__rec_loss !="MSE":
					logits_soft = tf.nn.softmax(px_logit[i], name='constrained')
					counts      = tf.reduce_sum(x_input_cast, -1)
					px_logit[i] = tf.log(tf.multiply(logits_soft, tf.tile(tf.reshape(counts, [tf.shape(counts)[0], 1]), [1, self.__original_dim])))
				
		y_prior_logit = tf.concat(y_prior_logit_lst, 1)
		y_prior = tf.nn.softmax(y_prior_logit, name='y_prob')
		
		# Negative entropy
		nent   = tf.reduce_sum(qy * tf.nn.log_softmax(qy_logit), 1)
		
		# KL divergence function for the categorical variable y
		kly    = nent - tf.reduce_sum(qy * tf.nn.log_softmax(y_prior_logit), 1)
		kly    = (1-self.__alpha)*kly
		losses = [None] * self.__num_gaussians
		klz    = [None] * self.__num_gaussians

		for i in range(self.__num_gaussians):
			losses[i], klz[i] = self.__labeled_loss(x_output, z[i], zm[i], tf.exp(zv[i]), zm_prior[i], tf.exp(zv_prior[i]), px_logit[i], ps_logit=ps_logit[i], pp_logit=pp_logit[i])

		# Recostruction error and KL divergence function
		lossMean = tf.add_n([qy[:, i] * losses[i] for i in range(self.__num_gaussians)])
		klzMean  = tf.add_n([qy[:, i] * klz[i] for i in range(self.__num_gaussians)])

		z_prior = [None] * self.__num_gaussians
		for i in range(self.__num_gaussians):
			prior_stddev = tf.sqrt(tf.exp(zv_prior[i]))
			z_prior[i]   = tf.random_normal(tf.stack([batch_size, self.__latent_layer]))
			z_prior[i]   = zm_prior[i] + tf.multiply(prior_stddev, z_prior[i]) #samples dalla prior
		
		# MMD divergence function
		mmdMean = tf.zeros(1, tf.float32)
		if (self.__alpha + self.__lambda - 1) != 0:
			mmdMean = self.__MMD(qy, z_prior, z, batch_size)
	  
		# Weighted KLz and MMD
		weightedKlzMean = (1 - self.__alpha) * klzMean
		weightedMmdMean = (self.__alpha + self.__lambda - 1) * mmdMean
		
		# Final loss function
		loss = tf.add_n([kly] + [lossMean] + [weightedKlzMean]) + weightedMmdMean
		
		gen_k = tf.placeholder(tf.float32,[1,self.__num_gaussians], name='gen_k')
		mu_y, logvar_y = self.__prior_z(gen_k)

		# Adam Optimizer to minimise the loss function
		train_step = tf.train.AdamOptimizer().minimize(loss)

		sess       = tf.Session()
		sess.run(tf.global_variables_initializer())

		if (1-self.__alpha) == 0:
			klzMean = tf.zeros(1, tf.float32)
		
		sess_info = (sess, qy_logit, nent, kly, lossMean, klzMean, mmdMean, loss, train_step)

		# Assigning the the values to private for further analyses and utilities. 
		self.__zm_prior = zm_prior
		self.__zv_prior = zv_prior
		self.__y_prior  = y_prior
		self.__px_logit = px_logit
		
		self.__zm = zm
		self.__zv = zv
		self.__qy = qy
		
		return sess_info

	# Public function to build the desidered AE
	def build(self):
		self.__sess_info = self.__build()
		
	# Function to train the selected AE
	def train(self, x_train, x_test, epochs=100, batch_size=100, x_train_out=None, max_patience=None, safe=True):

		# max_patience is used to obtain a early stop of the training phase

		# x_train can be a noise version of the original output
		# If only x_train is provided, it is assumed to be the desidered output
		if x_train_out is None:
			x_train_out = x_train

		zeros_train = np.where(~x_train.any(axis=1))[0]
		zeros_out   = np.where(~x_train_out.any(axis=1))[0]
		zeros_test  = np.where(~x_test.any(axis=1))[0]

		
		printed = False
		if len(zeros_train) > 0:
			print("* Warning! There are some cells with all genes equal to zeros")
			print("\t* x_train (%d cells):"%len(zeros_train), list(zeros_train))
			printed = True

		if len(zeros_out) > 0:
			if printed == False:
				print("* Warning! There are some cells with all genes equal to zeros")
				printed = True
			print("\t* x_train_out (%d cells):"%len(zeros_out), list(zeros_out))

		if len(zeros_test) > 0:
			if printed == False:
				print("* Warning! There are some cells with all genes equal to zeros")
				printed = True
			print("\t* x_test (%d cells):"%len(zeros_test), list(zeros_test))


		if printed:

			self.__zerosCells = {}
			self.__zerosCells["x_train"]     = zeros_train
			self.__zerosCells["x_train_out"] = zeros_out
			self.__zerosCells["x_test"]      = zeros_test

			if safe:
				print()
				print("* Consider to modify the selection of the genes used for AE")
				exit(-3)
			else:
				print()
				print("* Removing the cells with all genes equal to zeros ...")
				print("\t* You can retrieve this information using 'getZerosCells()'")
				print()

				if len(zeros_train) > 0:
					x_train = x_train[np.where(x_train.any(axis=1))[0]]
				if len(zeros_out) > 0:
					x_train_out = x_train_out[np.where(x_train_out.any(axis=1))[0]]
				if len(zeros_test) > 0:
					x_test = x_test[np.where(x_test.any(axis=1))[0]]
		
		if x_train.shape != x_train_out.shape:
			print('* x_train and x_train_out have different dimensions')
			exit(-4)

		(sess, qy_logit, nent, kly, lossMean, klzMean, mmdMean, loss, train_step) = self.__sess_info
	
		best_loss = None
		patience = 0
		
		for epoch in range(epochs):
			if self.__verbose:
				print(' * Epoch: ', self.__epoch+1)
			
			if len(x_train) < batch_size:
				batch_size_train = len(x_train)
			else:
				batch_size_train = batch_size
			
			if len(x_test) < batch_size:
				batch_size_test = len(x_test)
			else:
				batch_size_test = batch_size
			
			# Division of the training and test sets in batches
			total_batch_train   = int(len(x_train) / batch_size_train)
			x_batches_train     = np.array_split(x_train, total_batch_train)
			x_batches_train_out = np.array_split(x_train_out, total_batch_train)
			
			total_batch_test    = int(len(x_test) / batch_size_test)
			x_batches_test      = np.array_split(x_test, total_batch_test)
			
			# Cycling on the number of detected batches
			for i in range(total_batch_train):
				batch_x     = x_batches_train[i]
				batch_x_out = x_batches_train_out[i]
				sess.run(train_step, feed_dict={'x:0': batch_x, 'x_output:0': batch_x_out})
			 
			
			tr_kly, tr_rec, tr_klz, tr_mmd, tr_loss = np.zeros(5)
			t_kly, t_rec, t_klz, t_mmd, t_loss = np.zeros(5)
			
			# Calculating the terms of the ELBO function
			for i in range(total_batch_train):
				batch_x     = x_batches_train[i]
				batch_x_out = x_batches_train_out[i]
				tr_kly_batch, tr_rec_batch, tr_klz_batch, tr_mmd_batch, tr_loss_batch = sess.run([kly, lossMean, klzMean, mmdMean, loss], feed_dict={'x:0': batch_x, 'x_output:0': batch_x_out})
				tr_kly_batch, tr_rec_batch, tr_klz_batch, tr_mmd_batch, tr_loss_batch = tr_kly_batch.mean(), tr_rec_batch.mean(), tr_klz_batch.mean(), tr_mmd_batch.mean(), tr_loss_batch.mean()
				
				tr_kly  += tr_kly_batch
				tr_rec  += tr_rec_batch
				tr_klz  += tr_klz_batch
				tr_mmd  += tr_mmd_batch
				tr_loss += tr_loss_batch
			
			for i in range(total_batch_test):
				batch_x = x_batches_test[i]
				t_kly_batch, t_rec_batch, t_klz_batch, t_mmd_batch, t_loss_batch = sess.run([kly, lossMean, klzMean, mmdMean, loss], feed_dict={'x:0': batch_x, 'x_output:0': batch_x})
				t_kly_batch, t_rec_batch, t_klz_batch, t_mmd_batch, t_loss_batch = t_kly_batch.mean(),  t_rec_batch.mean(), t_klz_batch.mean(), t_mmd_batch.mean(), t_loss_batch.mean()
				
				t_kly   += t_kly_batch
				t_rec   += t_rec_batch
				t_klz   += t_klz_batch
				t_mmd   += t_mmd_batch
				t_loss  += t_loss_batch
				
			self.__epoch += 1
				
			tr_kly /= total_batch_train
			tr_rec /= total_batch_train
			tr_klz /= total_batch_train
			tr_mmd /= total_batch_train
			tr_loss /= total_batch_train
			
			t_kly /= total_batch_test
			t_rec /= total_batch_test
			t_klz /= total_batch_test
			t_mmd /= total_batch_test
			t_loss /= total_batch_test
			
			# Verbose modality to show the terms of the ELBO function
			if self.__verbose:
				string = (' {:>10s}, {:>10s}, {:>10s}, {:>10s}, {:>10s}, {:>10s}, {:>10s}, {:>10s}'.format('tr_kly', 'tr_klz', 'tr_mmd', 'tr_rec', 't_kly', 't_klz', 't_mmd', 't_rec'))
				print(string)

				string = (' {:10.4e}, {:10.4e}, {:10.4e}, {:10.4e}, {:10.4e}, {:10.4e}, {:10.4e}, {:10.4e}'.format(tr_kly, tr_klz, tr_mmd, tr_rec, t_kly, t_klz, t_mmd, t_rec))
				print(string)

				logits   = sess.run(qy_logit, feed_dict={'x:0': x_train})
				cat_pred = logits.argmax(1)
				unq_cluster, unq_cluster_fr = np.unique(cat_pred, return_counts=True)
				unq_cluster_fr = unq_cluster_fr/np.sum(unq_cluster_fr)
				print('\t tr_distinct clusters (%d): '%(len(unq_cluster)), unq_cluster)
				print('\t tr_distinct clusters %: ', np.round(unq_cluster_fr, decimals=2))

				logits = sess.run(qy_logit, feed_dict={'x:0': x_test})
				cat_pred = logits.argmax(1)
				unq_cluster, unq_cluster_fr = np.unique(cat_pred, return_counts=True)
				unq_cluster_fr = unq_cluster_fr/np.sum(unq_cluster_fr)
				print('\t t_distinct clusters (%d): '%(len(unq_cluster)), unq_cluster)
				print('\t t_distinct clusters %: ', np.round(unq_cluster_fr,decimals=2))
			
			# Saving the history of the AEs
			self.__history['train_kly'].append(tr_kly)
			self.__history['train_rec'].append(tr_rec)
			self.__history['train_klz'].append(tr_klz)
			self.__history['train_mmd'].append(tr_mmd)
			self.__history['train_loss'].append(tr_loss)
			
			self.__history['test_kly'].append(t_kly)
			self.__history['test_rec'].append(t_rec)
			self.__history['test_klz'].append(t_klz)
			self.__history['test_mmd'].append(t_mmd)
			self.__history['test_loss'].append(t_loss)
			
			# Check if a better loss value has been obtained
			if(best_loss is None or t_loss<best_loss):
				if self.__verbose:
					print(" * Train: %10.3f" %(tr_loss))
					print(" * Test:  %10.3f" %(t_loss))
					print(' * -> A better loss value has been found')
					print()
					print()
				
				# Update the best value of the loss, reset the patience counter 
				best_loss = t_loss
				patience=0
			else:
				if self.__verbose:
					print(" * Train: %10.3f" %(tr_loss))
					print(" * Test:  %10.3f" %(t_loss))
					print()
					print()
				
				# Increase the patience counter 
				patience+=1
			
			if(max_patience is not None and patience>=max_patience):
				return
			
	# Function to get a sample
	def __sample(self, learned_zm_prior, learned_zv_prior, i):
		
		mi = learned_zm_prior[i]
		mi = mi.reshape(self.__latent_layer)

		vi = np.exp(learned_zv_prior[i])
		vi = vi.reshape(self.__latent_layer)
		vi = np.diag(vi)

		zi = np.random.multivariate_normal(mean=mi,cov=vi)

		zi = zi.reshape((1, zi.shape[0]))

		return zi

	# Public function to sample new cells (i.e., synthetic cell generation)
	def sampling(self, num_samples=1):
		
		sess = self.__sess_info[0]
		
		z_sample = tf.placeholder(tf.float32,[1, self.__latent_layer], name='sample')
		y_sample = tf.constant(np.eye(self.__num_gaussians)[0], dtype=tf.float32)
		y_sample = tf.reshape(y_sample,(1,self.__num_gaussians))
		sampler  = self.__decoder(z_sample, y_sample)
					 
		learned_zm_prior = sess.run([self.__zm_prior], feed_dict={'x:0': np.zeros((1, self.__original_dim))})[0]
		learned_zv_prior = sess.run([self.__zv_prior], feed_dict={'x:0': np.zeros((1, self.__original_dim))})[0]
		
		sampled = np.zeros((num_samples, self.__original_dim))
		
		learned_y_prior = sess.run([self.__y_prior], feed_dict={'x:0': np.zeros((1, self.__original_dim))})[0][0]
		
		if self.__verbose:
			print("   * Weights of the prior distribution")
			for y in range(len(learned_y_prior)):
				print("\t* Distribution %d -> %.2f"%(y+1, 100*learned_y_prior[y]))
			print()

		for i in range(num_samples):
			c = np.random.choice(np.arange(0, self.__num_gaussians), p=learned_y_prior)
			zi = self.__sample(learned_zm_prior, learned_zv_prior, c)
			r = sess.run([sampler], feed_dict={z_sample.name: zi})[0][2][0]
			
			if self.__rec_loss in ["Poisson", "NB", "ZINB", "ZIP"]:
				if self.__constrained:
					r = np.exp(r)/sum(np.exp(r))
				else:
					r = np.exp(r)

				sampled[i] = r
			
			elif self.__rec_loss == "MSE":
				sampled[i] = r
		
		return sampled
	
	# Public function to get the reconstructed representation of the original cells
	def reconstructedRepresentation(self, data):
		
		sess = self.__sess_info[0]
		
		decod_x, pi_x  = sess.run([self.__px_logit, self.__qy], feed_dict={'x:0': data})
		
		decoded = np.zeros((data.shape))       

		for decode in range(decoded.shape[0]):
			for i in range(self.__num_gaussians):
				if self.__rec_loss == "MSE":
					decoded[decode] = decoded[decode] + (decod_x[i][decode])*pi_x[decode,i]
				else:
					decoded[decode] = decoded[decode] + np.exp(decod_x[i][decode])*pi_x[decode,i]
				
		
		return decoded
	
	# Public function to get the latent representation of the cells
	def latentRepresentation(self, data):
		
		sess = self.__sess_info[0]
		
		learned_zm = sess.run([self.__zm], feed_dict={'x:0': data})[0]
		learned_zv = sess.run([self.__zv], feed_dict={'x:0': data})[0]
		pi_x       = sess.run(self.__qy, feed_dict={'x:0': data})
		
		learned_zm = np.array(learned_zm)
		learned_zv = np.array(learned_zv)
		
		encoded = []

		for idx, pi in enumerate(pi_x):
			tmp = learned_zm[:, idx, :]

			value = np.zeros(tmp.shape[-1])
			for i in range(len(pi)):
				value += tmp[i,:]*pi[i]

			encoded.append(value)

		return np.array(encoded)

	def getZerosCells(self):
		return self.__zerosCells

	# Public function to obtain the history
	def getHistory(self):
		return self.__history

	# Public function to plot the different term of the ELBO function
	def plotLosses(self, width=5, height=5, show=True, folder=None, name=None):

		if name==None:
			name = "losses.pdf"
		else:
			name = name+"_losses.pdf"

		f, axs = plt.subplots(2,3,figsize=(width*3,height*2))

		sns.set(font_scale=1.1)
		sns.set_style("white")

		plt.rc('axes', labelsize=16)

		# ELBO function
		axs[0,0].plot(self.__history['train_loss'], linewidth=5)
		axs[0,0].plot(self.__history['test_loss'], linewidth=5)
		axs[0,0].set_xlabel("Epochs")
		axs[0,0].set_ylabel("Total loss")
		axs[0,0].legend(['Train', 'Test'], loc='upper right')

		# Reconstruction error
		axs[0,1].plot(self.__history['train_rec'], linewidth=5)
		axs[0,1].plot(self.__history['test_rec'], linewidth=5)
		axs[0,1].set_xlabel("Epochs")
		axs[0,1].set_ylabel("Reconstruction loss")

		# KLy error
		axs[0,2].plot(self.__history['train_kly'], linewidth=5)
		axs[0,2].plot(self.__history['test_kly'], linewidth=5)
		axs[0,2].set_xlabel("Epochs")
		axs[0,2].set_ylabel("KLy loss")

		
		# KLz error
		axs[1,0].plot(self.__history['train_klz'], linewidth=5)
		axs[1,0].plot(self.__history['test_klz'], linewidth=5)
		axs[1,0].set_xlabel("Epochs")
		axs[1,0].set_ylabel("KLz loss")

		# MMD error
		axs[1,1].plot(self.__history['train_mmd'], linewidth=5)
		axs[1,1].plot(self.__history['test_mmd'], linewidth=5)
		axs[1,1].set_xlabel("Epochs")
		axs[1,1].set_ylabel("MMD loss")

		f.delaxes(axs[1,2])

		plt.tight_layout()

		sns.despine(offset=10, trim=False)

		if show:
			plt.show(block=False)
		else:
			if folder is None:
				f.savefig('losses.pdf')
			else:
				if self.__verbose:
					print("   * Saving the generated plots to %s"%(folder+os.sep+name))
				f.savefig(folder+os.sep+name, bbox_inches='tight')

