from jit import types, dynjit
from jit.intrinsics import *
import types as pytypes
from collections.abc import Mapping

prim_types = {}


def ct2(ac):
    # noinspection PyTypeChecker
    try:
        a = prim_types.get(ac)
        if a is not None:
            return a
    except TypeError:
        # unhashable
        pass

    if isinstance(ac, pytypes.FunctionType):
        # noinspection PyUnresolvedReferences
        if ac.__closure__:
            raise NotImplementedError
        return types.FPtrT(ac)

    a = types.noms.get(type(ac))
    if a is not None:
        return a

    return types.TopT()


def ct1(ac):
    if isinstance(ac, tuple):
        return types.TupleT(tuple(map(ct2, ac)))
    if isinstance(ac, type):
        t = types.noms.get(ac)
        if t:
            return types.TypeT(t)
        return types.type_t
    return ct2(ac)


def ct(ac):
    if isinstance(ac, Mapping):
        fixed = ac.get("__fix__")
        if fixed:
            return types.RecordT({k: ct1(ac[k]) for k in fixed})

    return ct2(ac)


def define_prim(o):
    t = types.PrimT(o)
    v = dynjit.AbstractValue(dynjit.S(o), t)
    prim_types[o] = t
    return v


v_isinstance = define_prim(i_isinstance)
v_get_cells = define_prim(i_getcells)
v_py_call = define_prim(i_pycall)
v_getattr = define_prim(i_getattr)
v_add = define_prim(operator.add)
v_iadd = define_prim(i_iadd)
v_fadd = define_prim(i_fadd)
v_sconcat = define_prim(i_sconcat)
v_sext = define_prim(i_sext)
v_asbool = define_prim(i_asbool)
v_beq = define_prim(i_beq)
v_tupleget = define_prim(i_tupleget)
v_globals = define_prim(i_globals)
v_getitem = define_prim(i_getitem)
v_asint = define_prim(i_asint)
v_strunc = define_prim(i_strunc)
v_parseint = define_prim(i_parseint)
v_mkcell = define_prim(i_mkcell)
v_storeref = define_prim(i_store)
v_mkfunc = define_prim(i_mkfunc)
v_mkmethod = define_prim(i_mkmethod)
v_buildlist = define_prim(i_buildlist)
v_listappend = define_prim(list.append)


v_none = dynjit.AbstractValue(dynjit.S(None), types.none_t)


def mk_v_str(s: str):
    return dynjit.AbstractValue(dynjit.S(s), types.str_t)
