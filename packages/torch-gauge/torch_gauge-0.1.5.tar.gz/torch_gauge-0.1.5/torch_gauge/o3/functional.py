import torch


class NormContraction1d(torch.autograd.Function):
    """
    Calculate the (stabilized) channel-wise L2-norm of a 1d spherical tensor.

    The representation dimension must be an integer;
    the gradients at zero are enforced to be 0 by a non-negative eps.
    """

    @staticmethod
    def forward(
        ctx, data_ten: torch.Tensor, idx_ten: torch.LongTensor, out_shape, dim, eps
    ):
        """"""
        sum_sqr = torch.zeros(
            out_shape, device=data_ten.device, dtype=data_ten.dtype
        ).index_add_(dim, idx_ten, data_ten.pow(2))
        norm_shifted = (sum_sqr + eps ** 2).sqrt()
        ctx.dim = dim
        ctx.save_for_backward(data_ten, idx_ten, norm_shifted)
        return norm_shifted - eps

    @staticmethod
    def backward(ctx, grad_output):
        """"""
        data_ten, dst_ten, norm_shifted = ctx.saved_tensors
        gathered_grad_output = torch.index_select(
            grad_output, dim=ctx.dim, index=dst_ten
        )
        gathered_norm_shifted = torch.index_select(
            norm_shifted, dim=ctx.dim, index=dst_ten
        )
        norm_grad = data_ten / gathered_norm_shifted
        grad_input = gathered_grad_output * norm_grad
        return grad_input, None, None, None, None


class NormContraction2d(torch.autograd.Function):
    """
    Calculate the (stabilized) channel-wise L2 matrix-norm of a 2d spherical tensor.

    The representation dimensions must be a 2-tuple (i, i+1).
    """

    @staticmethod
    def forward(
        ctx,
        data_ten: torch.Tensor,
        idx_tens: torch.LongTensor,
        out_shape,
        dims,
        eps,
    ):
        """"""
        shape_rep_out = tuple(out_shape[d] for d in dims)
        cache_inds = (
            idx_tens[0] * shape_rep_out[1] + idx_tens[1]
        ).flatten()  # flattened dst indices
        sum_sqr = torch.zeros(
            out_shape,
            device=data_ten.device,
            dtype=data_ten.dtype,
        ).flatten(*dims)
        sum_sqr = sum_sqr.index_add_(
            dims[0], cache_inds, data_ten.flatten(*dims).pow(2)
        )
        norm_cache_shifted = (sum_sqr + eps ** 2).sqrt()
        norm_shifted = norm_cache_shifted.view(
            out_shape
        )  # must be contiguous at this point
        ctx.dims = dims
        ctx.save_for_backward(data_ten, cache_inds, norm_cache_shifted)
        return norm_shifted - eps

    @staticmethod
    def backward(ctx, grad_output):
        """"""
        data_ten, cache_inds, norm_cache = ctx.saved_tensors
        dims = ctx.dims
        gathered_grad_output = torch.index_select(
            grad_output.flatten(*dims),
            dim=dims[0],
            index=cache_inds,
        )
        gathered_norm_shifted = torch.index_select(
            norm_cache, dim=dims[0], index=cache_inds
        )
        gathered_norm_shifted = gathered_norm_shifted.view(data_ten.shape)
        norm_grad = data_ten / gathered_norm_shifted
        grad_input = gathered_grad_output.view_as(norm_grad) * norm_grad
        return grad_input, None, None, None, None
