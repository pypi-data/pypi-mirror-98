import ctypes
import numpy as np
import pytest

from psyneulink.core import llvm as pnlvm

from llvmlite import ir


ITERATIONS=100
DIM_X=1000

matrix = np.random.rand(DIM_X, DIM_X)
vector = np.random.rand(DIM_X)
llvm_res = np.random.rand(DIM_X)

x, y = matrix.shape

@pytest.mark.llvm
@pytest.mark.parametrize('mode', ['CPU',
                                  pytest.param('PTX', marks=pytest.mark.cuda)])
def test_fixed_dimensions__pnl_builtin_vxm(mode):
    # The original builtin mxv function
    binf = pnlvm.LLVMBinaryFunction.get("__pnl_builtin_vxm")
    orig_res = np.empty_like(llvm_res)
    if mode == 'CPU':
        ct_in_ty, ct_mat_ty, _, _, ct_res_ty = binf.byref_arg_types

        ct_vec = vector.ctypes.data_as(ctypes.POINTER(ct_in_ty))
        ct_mat = matrix.ctypes.data_as(ctypes.POINTER(ct_mat_ty))
        ct_res = orig_res.ctypes.data_as(ctypes.POINTER(ct_res_ty))

        binf.c_func(ct_vec, ct_mat, x, y, ct_res)
    else:
        binf.cuda_wrap_call(vector, matrix, np.int32(x), np.int32(y), orig_res)

    custom_name = None

    with pnlvm.LLVMBuilderContext() as ctx:
        custom_name = ctx.get_unique_name("vxsqm")
        double_ptr_ty = ctx.convert_python_struct_to_llvm_ir(1.0).as_pointer()
        func_ty = ir.FunctionType(ir.VoidType(), (double_ptr_ty, double_ptr_ty, double_ptr_ty))

        # get builtin IR
        builtin = ctx.import_llvm_function("__pnl_builtin_vxm")

        # Create square vector matrix multiply
        function = ir.Function(ctx.module, func_ty, name=custom_name)
        _x = ctx.int32_ty(x)
        _v, _m, _o = function.args
        block = function.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        builder.call(builtin, [_v, _m, _x, _x, _o])
        builder.ret_void()

    binf2 = pnlvm.LLVMBinaryFunction.get(custom_name)
    new_res = np.empty_like(llvm_res)

    if mode == 'CPU':
        ct_res = new_res.ctypes.data_as(ctypes.POINTER(ct_res_ty))

        binf2(ct_vec, ct_mat, ct_res)
    else:
        binf2.cuda_wrap_call(vector, matrix, new_res)

    assert np.array_equal(orig_res, new_res)


@pytest.mark.llvm
@pytest.mark.parametrize('mode', ['CPU',
                                  pytest.param('PTX', marks=pytest.mark.cuda)])
@pytest.mark.parametrize('val', [np.int8(0x7e),
                                 np.int16(0x7eec),
                                 np.int32(0x7eedbeee),
                                 np.int64(0x7eedcafedeadbeee)
                                ], ids=lambda x: str(x.dtype))
def test_integer_broadcast(mode, val):
    custom_name = None
    with pnlvm.LLVMBuilderContext() as ctx:
        custom_name = ctx.get_unique_name("broadcast")
        int_ty = ctx.convert_python_struct_to_llvm_ir(val)
        int_array_ty = ir.ArrayType(int_ty, 8)
        func_ty = ir.FunctionType(ir.VoidType(), (int_ty.as_pointer(),
                                                  int_array_ty.as_pointer()))
        function = ir.Function(ctx.module, func_ty, name=custom_name)

        i, o = function.args
        block = function.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        ival = builder.load(i)
        ival = builder.add(ival, ival.type(1))
        with pnlvm.helpers.array_ptr_loop(builder, o, "broadcast") as (b, i):
            out_ptr = builder.gep(o, [ctx.int32_ty(0), i])
            builder.store(ival, out_ptr)
        builder.ret_void()

    binf = pnlvm.LLVMBinaryFunction.get(custom_name)
    res = np.zeros(8, dtype=val.dtype)

    if mode == 'CPU':
        ct_res = np.ctypeslib.as_ctypes(res)
        ct_in = np.ctypeslib.as_ctypes(val)

        binf(ctypes.byref(ct_in), ctypes.byref(ct_res))
    else:
        binf.cuda_wrap_call(np.asarray(val), res)

    assert all(res == np.broadcast_to(val + 1, 8))
