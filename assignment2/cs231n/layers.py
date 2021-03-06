from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    N = x.shape[0]
    x_flat = x.reshape(N, -1) # NxD
    out = x_flat.dot(w) + b
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = np.zeros_like(x), np.zeros_like(w), np.zeros_like(b)
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    N, M = dout.shape
    D = w.shape[0]

    dx = dout.dot(w.T).reshape(x.shape)

    dw = x.reshape(N,D).T.dot(dout)
    # dw = \
    # np.sum( # DxM
    #     np.repeat( # NxDxM
    #         np.reshape( # Nx1xM
    #             dout, # NxM
    #             (N,1,M)),
    #         D, axis=1) * \
    #     np.repeat( # NxDxM
    #         np.reshape( # NxDx1
    #             x, # NxD1xD2x...xDk
    #             (N,D,1)),
    #         M, axis=2),
    #     axis=0)

    db = np.sum(dout, axis=0)

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    out = np.maximum(0, x)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    dx = (x > 0.) * dout
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #######################################################################
        sample_mean = np.mean(x, axis=0)
        sample_var = np.var(x, axis=0)
        out = gamma * (x - sample_mean) / np.sqrt(sample_var + eps) + beta

        running_mean = momentum * running_mean + (1 - momentum) * sample_mean
        running_var = momentum * running_var + (1 - momentum) * sample_var

        cache = x, gamma, beta, sample_mean, sample_var, eps
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        out = gamma * (x - running_mean) / np.sqrt(running_var + eps) + beta
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    x, gamma, beta, sample_mean, sample_var, eps = cache
    N, D = x.shape
    dx, dgamma, dbeta = np.zeros_like(x), np.zeros((D,), dtype=x.dtype), np.zeros((D,), dtype=x.dtype)
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    ###########################################################################
    # This is how the derivatives are calculated:
    # dL/dx_d^i = sum_ii=1..n( dout[ii, d] * (dout/dx)[ii,d] )
    for d in range(D):
        for i in range(N):
            noti = np.arange(N) != i
            num = x[:,d] - sample_mean[d]
            denum = np.sqrt(sample_var[d] + eps)

            doutdx = np.zeros((N,)) * 1.
            dnum = np.zeros((N,)) * 1.

            dnum[noti] = -1./N
            dnum[i] = 1. - 1./N
            ddenum = (x[i,d] - sample_mean[d]) / np.sqrt(sample_var[d] + eps)
            ddenum /= N

            doutdx = gamma[d] * (denum * dnum - num * ddenum) / denum**2
            dx[i,d] = np.sum(dout[:, d] * doutdx)

    x_norm = (x - sample_mean) / np.sqrt(sample_var + eps)
    dgamma = np.sum(dout * x_norm, axis=0)

    dbeta = np.sum(dout, axis=0)

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass.

    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    x, gamma, beta, sample_mean, sample_var, eps = cache
    N, D = x.shape
    dx, dgamma, dbeta = np.zeros_like(x), np.zeros((D,), dtype=x.dtype), np.zeros((D,), dtype=x.dtype)
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    ###########################################################################
    num = x-sample_mean
    denum = np.sqrt(sample_var + eps)
    denum3 = denum**3
    A = (num*dout).sum(axis=0)
    B = dout.sum(axis=0)
    for i in range(N):
        sum1 = -1./N*B + dout[i]
        sum1 /= denum
        sum2 = -1./N*num[i]*A
        sum2 /= denum3
        dx[i]=sum1+sum2
    dx *= gamma

    x_norm = (x - sample_mean) / np.sqrt(sample_var + eps)
    dgamma = np.sum(dout * x_norm, axis=0)

    dbeta = np.sum(dout, axis=0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We drop each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        mask = np.random.rand(*x.shape) > p
        out = mask * x / (1. - p)
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        out = x
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        dx = dout * mask / (1. - dropout_param['p'])
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == 'test':
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width HH.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    stride, pad = conv_param['stride'], conv_param['pad']
    N, C, H, W = x.shape
    F, C, HH, WW = w.shape
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    def get_patch(n, i, j):
        return x_pad[n, :,
               i * stride : i * stride + HH,
               j * stride : j * stride + WW]

    H_ = 1 + int((H + 2 * pad - HH) / stride)
    W_ = 1 + int((W + 2 * pad - WW) / stride)
    x_pad = np.pad(x, pad_width=((0,0),(0,0),(pad,pad),(pad,pad)), mode='constant')
    out = np.zeros((N, F, H_, W_), dtype=x.dtype)
    for n in range(N):
        for f in range(F):
            for i in range(H_):
                for j in range(W_):
                    patch = get_patch(n, i, j)
                    out[n, f, i, j] = (w[f] * patch).sum() + b[f]

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    x, w, b, conv_param = cache
    dw = np.zeros_like(w)
    db = np.zeros_like(b)
    dx = np.zeros_like(x)

    # dx
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    _, _, H_, W_ = dout.shape
    stride, pad = conv_param['stride'], conv_param['pad']
    for n in range(N):
        for f in range(F):
            for i_ in range(H_):
                for j_ in range(W_):
                    for ii in range(HH):
                        for jj in range(WW):
                            i = i_ * stride + ii - pad
                            j = j_ * stride + jj - pad
                            if 0 <= i < H and 0 <= j < W:
                                dx[n, :, i, j] += w[f, :, ii, jj] * dout[n, f, i_, j_]
                                dw[f, :, ii, jj] += x[n, :, i, j] * dout[n, f, i_, j_]
                    db[f] += dout[n, f, i_, j_].sum()
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    Returns a tuple of:
    - out: Output data
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max pooling forward pass                            #
    ###########################################################################
    stride, HH, WW = pool_param['stride'], pool_param['pool_height'], pool_param['pool_width']
    N, C, H, W = x.shape

    def get_patch(n, i, j):
        return x[n, :,
               i * stride : i * stride + HH,
               j * stride : j * stride + WW]

    H_ = 1 + int((H - HH) / stride)
    W_ = 1 + int((W - WW) / stride)

    out = np.zeros((N, C, H_, W_), dtype=x.dtype)
    for n in range(N):
        for i in range(H_):
            for j in range(W_):
                patch = get_patch(n, i, j)
                out[n, :, i, j] = np.transpose(patch.reshape(C,-1), axes=(1,0)).max(axis=0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    ###########################################################################
    # TODO: Implement the max pooling backward pass                           #
    ###########################################################################
    x, pool_param = cache
    stride, HH, WW = pool_param['stride'], pool_param['pool_height'], pool_param['pool_width']
    N, C, H, W = x.shape
    _, _, H_, W_ = dout.shape

    def get_patch(n, i_, j_):
        return x[n, :,
               i_ * stride : i_ * stride + HH,
               j_ * stride : j_ * stride + WW]

    dx = np.zeros_like(x)

    for n in range(N):
        for i_ in range(H_):
            for j_ in range(W_):
                patch = get_patch(n, i_, j_)
                ind = np.argmax(patch.reshape(C,-1), axis=1) # C
                i = i_ * stride + ind / WW # C
                j = j_ * stride + ind % WW # C
                for c in range(C):
                    dx[n, c, int(i[c]), int(j[c])] += dout[n, c, i_, j_]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    eps = 1e-9
    momentum = 0.9

    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization using the vanilla   #
    # version of batch normalization defined above. Your implementation should#
    # be very short; ours is less than five lines.                            #
    ###########################################################################
    sample_mean = np.mean(x, axis=(0, 2, 3)).reshape(1, x.shape[1], 1, 1)
    sample_var = np.var(x, axis=(0, 2, 3)).reshape(1, x.shape[1], 1, 1)
    gamma = gamma.reshape(1, x.shape[1], 1, 1)
    beta = beta.reshape(1, x.shape[1], 1, 1)
    out = gamma * (x - sample_mean) / np.sqrt(sample_var + eps) + beta

    #running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    #running_var = momentum * running_var + (1 - momentum) * sample_var

    cache = x, gamma, beta, sample_mean, sample_var, eps
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    x, gamma, beta, sample_mean, sample_var, eps = cache
    N, C, H, W = x.shape
    dx, dgamma, dbeta = np.zeros_like(x), np.zeros((C,), dtype=x.dtype), np.zeros((C,), dtype=x.dtype)
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    ###########################################################################
    # FIXME dx is not correct, check derivatives
    for c in range(C):
        for i in range(N):
            noti = np.arange(N) != i
            num = x[:,c] - sample_mean[:,c]
            denum = np.sqrt(sample_var[:,c] + eps)

            doutdx = np.zeros((N,H,W)) * 1.
            dnum = np.zeros((N,H,W)) * 1.

            dnum[noti] = -1./(N*H*W)
            dnum[i] = 1. - 1./(N*H*W)
            ddenum = (x[i,c] - sample_mean[:,c]) / np.sqrt(sample_var[:,c] + eps)
            ddenum /= N*H*W

            # print (gamma.shape)
            # print (denum.shape)
            # print (dnum.shape)
            # print (num.shape)
            # print (ddenum.shape)
            doutdx = gamma[:,c] * (denum * dnum - num * ddenum) / denum**2
            dx[i,c] = np.sum(dout[:, c] * doutdx)

    x_norm = (x - sample_mean) / np.sqrt(sample_var + eps)
    dgamma = np.sum(dout * x_norm, axis=(0,2,3))

    dbeta = np.sum(dout, axis=(0,2,3))

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx


def softmax(x):
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    return shifted_logits / Z