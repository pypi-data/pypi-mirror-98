#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <math.h>
#include "longobject.h"
#include "structmember.h"
#include "eq.h"


typedef struct {
    PyObject_HEAD
    size_t n_bins;
    float min;               /* size of hashtable array*/
    float max;               /* size of hashtable array*/
    float width;
    PyObject **items;
} BinsObject;

static PyObject *indexerr = NULL;

static inline int
valid_index(Py_ssize_t i, Py_ssize_t limit)
{
    /* The cast to size_t lets us use just a single comparison
       to check whether i is in the range: 0 <= i < limit.
       See:  Section 14.2 "Bounds Checking" in the Agner Fog
       optimization manual found at:
       https://www.agner.org/optimize/optimizing_cpp.pdf
    */
    return (size_t) i < (size_t) limit;
}


static Py_ssize_t _Py_HOT_FUNCTION
get_bin(const BinsObject *op, double value)
{
    if (value <= op->min){
        return 0;
    }
    if (value >= op->max){
        return op->n_bins - 1;
    }
    double d_bin = value / op->width;
    if (d_bin - (size_t)(d_bin) > 0.5)
        d_bin += 1.0;
    Py_ssize_t bin = (int)(d_bin);

    return bin;

}

static Py_ssize_t _Py_HOT_FUNCTION
nearest(const BinsObject *op, int bin)
{
    Py_ssize_t nearest_right = -1;
    Py_ssize_t nearest_left = -1;

    if (bin < op->n_bins-1){
        for (Py_ssize_t idx = bin+1; idx < op->n_bins; idx++){

            if (op->items[idx] != NULL){
                nearest_right = idx;
                break;
            }
        }
    }

    if (bin > 0){
        for (Py_ssize_t idx = bin-1; idx >= 0; idx--){
                if (op->items[idx] != NULL){
                    nearest_left = idx;
                    break;
                }
            }
    }

    if (nearest_left < 0)
        return nearest_right;

    if (nearest_right < 0)
        return nearest_left;

    if (nearest_right-bin < bin-nearest_left)
        return nearest_right;

    return nearest_left;
}


static PyObject *
Bins_item(BinsObject *a, Py_ssize_t i)
{
    if (!valid_index(i, a->n_bins)) {
        if (indexerr == NULL) {
            indexerr = PyUnicode_FromString(
                "Bins index out of range");
            if (indexerr == NULL)
                return NULL;
        }
        PyErr_SetObject(PyExc_IndexError, indexerr);
        return NULL;
    }
    if (a->items[i] == NULL)
        a->items[i] = Py_None;
    Py_INCREF(a->items[i]);
    return a->items[i];
}

static int
_Bins_clear(BinsObject *a)
{
    Py_ssize_t i;
    PyObject **items = a->items;
    if (items != NULL) {
        /* Because XDECREF can recursively invoke operations on
           this list, we make it empty first. */
        i = Py_SIZE(a);
        a->n_bins = 0;
        a->items = NULL;
        while (--i >= 0) {
            Py_XDECREF(items[i]);
        }
        PyMem_Free(items);
    }
    /* Never fails; the return value can be ignored.
       Note that there is no guarantee that the list is actually empty
       at this point, because XDECREF may have populated it again! */
    return 0;
}

static int
Bins_resize(BinsObject *self, Py_ssize_t newsize)
{
    PyObject **items;
    size_t num_allocated_bytes;
    Py_ssize_t allocated = self->n_bins;

    /* Bypass realloc() when a previous overallocation is large enough
       to accommodate the newsize.  If the newsize falls lower than half
       the allocated size, then proceed with the realloc() to shrink the list.
    */
    if (allocated >= newsize && newsize >= (allocated >> 1)) {
        assert(self->items != NULL || newsize == 0);
        return 0;
    }

    num_allocated_bytes = newsize * sizeof(PyObject *);
    items = (PyObject **)PyMem_Realloc(self->items, num_allocated_bytes);
    if (items == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    self->items = items;
    self->n_bins = newsize;

    return 0;
}

static PyObject *
Bins_slice(BinsObject *a, Py_ssize_t ilow, Py_ssize_t ihigh)
{
    PyObject *dest;
    PyObject **src;
    Py_ssize_t i, len;
    len = ihigh - ilow;
    dest = PyList_New(len);
    if (dest == NULL)
        return NULL;
    src = a->items + ilow;
    for (i = 0; i < len; i++) {
        if (src[i] == NULL){
            src[i] = Py_None;
        }
        PyObject *v = src[i];
        Py_INCREF(v);
        PyList_SetItem(dest, i, v);
    }
    return (PyObject *)dest;
}

static int
Bins_ass_slice(BinsObject *a, Py_ssize_t ilow, Py_ssize_t ihigh, PyObject *v)
{
    /* Because [X]DECREF can recursively invoke list operations on
       this list, we must postpone all [X]DECREF activity until
       after the list is back in its canonical shape.  Therefore
       we must allocate an additional array, 'recycle', into which
       we temporarily copy the items that are deleted from the
       list. :-( */
    PyObject *recycle_on_stack[8];
    PyObject **recycle = recycle_on_stack; /* will allocate more if needed */
    PyObject **items;
    PyObject **vitem = NULL;
    PyObject *v_as_SF = NULL; /* PySequence_Fast(v) */
    Py_ssize_t n; /* # of elements in replacement list */
    Py_ssize_t norig; /* # of elements in list getting replaced */
    Py_ssize_t d; /* Change in size */
    Py_ssize_t k;
    size_t s;
    int result = -1;            /* guilty until proved innocent */
#define b ((BinsObject *)v)
    if (v == NULL)
        n = 0;
    else {
        if (a == b) {
            /* Special case "a[i:j] = a" -- copy b first */
            v = Bins_slice(b, 0, Py_SIZE(b));
            if (v == NULL)
                return result;
            result = Bins_ass_slice(a, ilow, ihigh, v);
            Py_DECREF(v);
            return result;
        }
        v_as_SF = PySequence_Fast(v, "can only assign an iterable");
        if(v_as_SF == NULL)
            goto Error;
        n = PySequence_Fast_GET_SIZE(v_as_SF);
        vitem = PySequence_Fast_ITEMS(v_as_SF);
    }
    if (ilow < 0)
        ilow = 0;
    else if (ilow > Py_SIZE(a))
        ilow = Py_SIZE(a);

    if (ihigh < ilow)
        ihigh = ilow;
    else if (ihigh > Py_SIZE(a))
        ihigh = Py_SIZE(a);

    norig = ihigh - ilow;
    assert(norig >= 0);
    d = n - norig;
    if (Py_SIZE(a) + d == 0) {
        Py_XDECREF(v_as_SF);
        return _Bins_clear(a);
    }
    items = a->items;
    /* recycle the items that we are about to remove */
    s = norig * sizeof(PyObject *);
    /* If norig == 0, item might be NULL, in which case we may not memcpy from it. */
    if (s) {
        if (s > sizeof(recycle_on_stack)) {
            recycle = (PyObject **)PyMem_Malloc(s);
            if (recycle == NULL) {
                PyErr_NoMemory();
                goto Error;
            }
        }
        memcpy(recycle, &items[ilow], s);
    }

    if (d < 0) { /* Delete -d items */
        Py_ssize_t tail;
        tail = (Py_SIZE(a) - ihigh) * sizeof(PyObject *);
        memmove(&items[ihigh+d], &items[ihigh], tail);
        if (Bins_resize(a, Py_SIZE(a) + d) < 0) {
            memmove(&items[ihigh], &items[ihigh+d], tail);
            memcpy(&items[ilow], recycle, s);
            goto Error;
        }
        items = a->items;
    }
    else if (d > 0) { /* Insert d items */
        k = Py_SIZE(a);
        if (Bins_resize(a, k+d) < 0)
            goto Error;
        items = a->items;
        memmove(&items[ihigh+d], &items[ihigh],
            (k - ihigh)*sizeof(PyObject *));
    }
    for (k = 0; k < n; k++, ilow++) {
        PyObject *w = vitem[k];
        Py_XINCREF(w);
        items[ilow] = w;
    }
    for (k = norig - 1; k >= 0; --k)
        Py_XDECREF(recycle[k]);
    result = 0;
 Error:
    if (recycle != recycle_on_stack)
        PyMem_Free(recycle);
    Py_XDECREF(v_as_SF);
    return result;
#undef b
}

static Py_ssize_t
Bins_length(PyListObject *a)
{
    return Py_SIZE(a);
}

static Py_ssize_t
put(const BinsObject *op, Py_ssize_t idx, PyObject *item)
{
    if (item == NULL)
        return -1;

    if (idx < 0 || idx >= op->n_bins)
        return -1;

    PyObject* tmp = op->items[idx];
    if (tmp != NULL)
        Py_DECREF(tmp);

    Py_INCREF(item);
    op->items[idx] = item;
    return idx;

}

static Py_ssize_t
get_item(const BinsObject *op, size_t idx, PyObject **item_addr)
{

    if (idx < 0 || idx >= op->n_bins){
        Py_INCREF(Py_None);
        *item_addr = Py_None;
        return -1;
    }
    PyObject* item = op->items[idx];
    if (item != NULL) {
        Py_INCREF(item);
        *item_addr = item;
    } else {
        Py_INCREF(Py_None);
        *item_addr = Py_None;
    }
    return idx;
}

static PyObject *
Bins_subscript(BinsObject* self, PyObject* item)
{
    if (PyIndex_Check(item)) {
        Py_ssize_t i;
        i = PyNumber_AsSsize_t(item, PyExc_IndexError);
        if (i == -1 && PyErr_Occurred())
            return NULL;
        if (i < 0)
            i += self->n_bins;
        return Bins_item(self, i);
    }
    else if (PySlice_Check(item)) {
        Py_ssize_t start, stop, step, slicelength, i;
        size_t cur;
        PyObject* result;
        PyObject* it;
        PyObject **src;
        PyObject **dest;

        if (PySlice_Unpack(item, &start, &stop, &step) < 0) {
            return NULL;
        }

        slicelength = PySlice_AdjustIndices(Py_SIZE(self), &start, &stop,
                                            step);

        if (slicelength <= 0) {
            return PyList_New(0);
        }
        else if (step == 1) {
            return Bins_slice(self, start, stop);
        }
        else {
            result = PyList_New(slicelength);
            if (!result) return NULL;
            src = self->items;
            for (cur = start, i = 0; i < slicelength;
                 cur += (size_t)step, i++) {
                it = src[cur];
                Py_INCREF(it);
                PyList_SetItem(result, i, it);
            }
            return result;
        }
    }
    else {
        PyErr_Format(PyExc_TypeError,
                     "indices must be integers or slices, not %.200s",
                     Py_TYPE(item)->tp_name);
        return NULL;
    }
}

PyObject*
Bins_bin(BinsObject* self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *value = args[0];
    double d_value = PyFloat_AsDouble(value);
    return PyLong_FromLong(get_bin(self, d_value));
}

PyObject*
Bins_bin_nearest(BinsObject* self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject *value = args[0];
    double d_value = PyFloat_AsDouble(value);
    return PyLong_FromLong(get_bin(self, d_value));
}

PyObject * _Py_HOT_FUNCTION
Bins_put(BinsObject* self, PyObject *const *args, Py_ssize_t nargs)
{
    double value;
    Py_ssize_t idx = -1;
	if (PyFloat_Check(args[0]))
	    value = PyFloat_AsDouble(args[0]);
	else if (PyLong_Check(args[0]))
	    value = PyLong_AsDouble(args[0]);
	else
	    return PyLong_FromLong(idx);
    PyObject* item = args[1];
	idx = get_bin(self, value);
	if (idx >= 0 && idx < self->n_bins){
        idx = put(self, idx, item);
    }
    PyObject* ret = PyLong_FromLong(idx);
	return ret;
}

PyObject * _Py_HOT_FUNCTION
Bins_get(BinsObject* self, PyObject *const *args, Py_ssize_t nargs)
{
	double value;
	PyObject* item = NULL;
	Py_ssize_t bin = -1;

	if (PyLong_Check(args[0])){
	    value = PyLong_AsDouble(args[0]);
	} else if (PyFloat_Check(args[0])) {
	    value = PyFloat_AsDouble(args[0]);
    } else {
        return Py_BuildValue("(Oi)", Py_None, bin);
    }
    bin = get_bin(self, value);
	bin = get_item(self, bin, &item);
	return Py_BuildValue("(Oi)", item, bin);
}

static void
Bins_dealloc(BinsObject* self)
{
    Py_XDECREF(self->items);
	Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject*
Bins_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    BinsObject* self;
    self = (BinsObject*)type->tp_alloc(type, 0);
    return (PyObject*)self;
}


static PyObject *
Bins_sizeof(BinsObject *self, PyObject* Py_UNUSED(ignored))
{
    Py_ssize_t res;
    res = _PyObject_SIZE(Py_TYPE(self)) + self->n_bins * sizeof(void*);
    return PyLong_FromSsize_t(res);
}

static int
Bins_preallocate_exact(BinsObject *self, Py_ssize_t n_bins)
{
    assert(self->items == NULL);
    assert(n_bins > 0);

    PyObject **items = PyMem_New(PyObject*, n_bins);
    if (items == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    self->items = items;
    self->n_bins = n_bins;
    return 0;
}

static int
Bins_init(BinsObject* self, PyObject* args, PyObject* kwds)
{
    static char* kwlist[] = {"min", "max", "width", NULL};

    PyObject* items = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "fff", kwlist,
        &self->min,
        &self->max,
        &self->width,
        &items))
        return -1;

    if (self->max <= self->min){
        PyErr_SetString(PyExc_AttributeError,"Max must be greater than min");
        return -1;
    }

    if (self->width >= (self->max-self->min)){
        PyErr_SetString(PyExc_AttributeError, "Width must be less than difference between max and min");
        return -1;
    }

    self->n_bins = (Py_ssize_t)(int)((self->max - self->min)/self->width)+1;

    if (self->n_bins < 2)
        self->n_bins = 2;

    self->items = calloc(self->n_bins, sizeof(PyObject *));
    //return Bins_preallocate_exact(self, n_bins);

    /*if (PyList_Check(items)){
        Py_ssize_t n = PyList_Size(items);
        if (n <= self->n_bins){
            for (Py_ssize_t idx=0; idx < n; idx++){
                PyObject * item = PyList_GetItem(items, idx);
                if (item != NULL){
                    put(self, idx, item);
                }
            }
            return 0;
        } else
            PyErr_SetString(PyExc_AttributeError,"Items length greater than number of bins");
    }
    if (PyIter_Check(items)){
        for (Py_ssize_t idx = 0;  idx < self->n_bins; idx++){
            PyObject* item = PyIter_Next(items);
            put(self, idx, item);
        }
        return 0;
    }
    PyErr_SetString(PyExc_AttributeError,"Items must be list or support iterator protocol");
    return -1;
    */
    return 0;
}

static int
Bins_ass_item(BinsObject *a, Py_ssize_t i, PyObject *v)
{
    if (i > a->n_bins - 1) {
        PyErr_SetString(PyExc_IndexError,
                        "Bins assignment index out of range");
        return -1;
    }
    if (v == NULL)
        return Bins_ass_slice(a, i, i+1, v);
    Py_INCREF(v);
    if (a->items[i] == NULL){
        a->items[i] = v;
    }
    else {
        Py_SETREF(a->items[i], v);
    }
    return 0;
}

static int
Bins_ass_subscript(BinsObject* self, PyObject* item, PyObject* value)
{
    if(PyIndex_Check(item)) {
        Py_ssize_t i = PyNumber_AsSsize_t(item, PyExc_IndexError);
        if (i == -1 && PyErr_Occurred())
            return -1;
        if (i < 0)
            i += self->n_bins;
        return Bins_ass_item(self, i, value);
    }
    else if (PySlice_Check(item)) {
        Py_ssize_t start, stop, step, slicelength;
        if (PySlice_Unpack(item, &start, &stop, &step) < 0) {
            return -1;
        }
        slicelength = PySlice_AdjustIndices(Py_SIZE(self), &start, &stop,
                                            step);
        if (step == 1)
            return Bins_ass_slice(self, start, stop, value);

        /* Make sure s[5:2] = [..] inserts at the right place:
           before 5, not before 2. */
        if ((step < 0 && start < stop) ||
            (step > 0 && start > stop))
            stop = start;

        if (value == NULL) {
            /* delete slice */
            PyObject **garbage;
            size_t cur;
            Py_ssize_t i;
            int res;

            if (slicelength <= 0)
                return 0;

            if (step < 0) {
                stop = start + 1;
                start = stop + step*(slicelength - 1) - 1;
                step = -step;
            }

            garbage = (PyObject**)
                PyMem_Malloc(slicelength*sizeof(PyObject*));
            if (!garbage) {
                PyErr_NoMemory();
                return -1;
            }

            /* drawing pictures might help understand these for
               loops. Basically, we memmove the parts of the
               Bins that are *not* part of the slice: step-1
               items for each item that is part of the slice,
               and then tail end of the list that was not
               covered by the slice */
            for (cur = start, i = 0;
                 cur < (size_t)stop;
                 cur += step, i++) {
                Py_ssize_t lim = step - 1;

                garbage[i] = Bins_item(self, i);

                if (cur + step >= (size_t)Py_SIZE(self)) {
                    lim = Py_SIZE(self) - cur - 1;
                }

                memmove(self->items + cur - i,
                    self->items + cur + 1,
                    lim * sizeof(PyObject *));
            }
            cur = start + (size_t)slicelength * step;
            if (cur < (size_t)Py_SIZE(self)) {
                memmove(self->items + cur - slicelength,
                    self->items + cur,
                    (Py_SIZE(self) - cur) *
                     sizeof(PyObject *));
            }

            res = Bins_resize(self, Py_SIZE(self));

            for (i = 0; i < slicelength; i++) {
                Py_DECREF(garbage[i]);
            }
            PyMem_Free(garbage);

            return res;
        }
        else {
            /* assign slice */
            PyObject *ins, *seq;
            PyObject **garbage, **seqitems, **selfitems;
            Py_ssize_t i;
            size_t cur;

            seq = PyList_GetSlice(value, 0, PyList_GET_SIZE(value));
            if (!seq)
                return -1;

            if (PySequence_Fast_GET_SIZE(seq) != slicelength) {
                PyErr_Format(PyExc_ValueError,
                    "attempt to assign sequence of "
                    "size %zd to extended slice of "
                    "size %zd",
                         PySequence_Fast_GET_SIZE(seq),
                         slicelength);
                Py_DECREF(seq);
                return -1;
            }

            if (!slicelength) {
                Py_DECREF(seq);
                return 0;
            }

            garbage = (PyObject**)
                PyMem_Malloc(slicelength*sizeof(PyObject*));
            if (!garbage) {
                Py_DECREF(seq);
                PyErr_NoMemory();
                return -1;
            }

            selfitems = self->items;
            seqitems = PySequence_Fast_ITEMS(seq);
            for (cur = start, i = 0; i < slicelength;
                 cur += (size_t)step, i++) {
                garbage[i] = selfitems[cur];
                ins = seqitems[i];
                Py_INCREF(ins);
                selfitems[cur] = ins;
            }

            for (i = 0; i < slicelength; i++) {
                Py_DECREF(garbage[i]);
            }

            PyMem_Free(garbage);
            Py_DECREF(seq);

            return 0;
        }
    }
    else {
        PyErr_Format(PyExc_TypeError,
                     "Bins indices must be integers or slices, not %.200s",
                     Py_TYPE(item)->tp_name);
        return -1;
    }
}

static PyMappingMethods Bins_as_mapping = {
    (lenfunc)Bins_length,
    (binaryfunc)Bins_subscript,
    (objobjargproc)Bins_ass_subscript
};

static PySequenceMethods Bins_as_sequence = {
    (lenfunc)Bins_length,                       /* sq_length */
    0, //(binaryfunc)Bins_concat,               /* sq_concat */
    0, //(ssizeargfunc)Bins_repeat,             /* sq_repeat */
    (ssizeargfunc)Bins_item,                    /* sq_item */
    (ssizeargfunc)Bins_subscript,               /* sq_slice */
    (ssizeobjargproc)Bins_ass_item,             /* sq_ass_item */
    (ssizeobjargproc)Bins_ass_subscript,        /* sq_ass_slice */
    0, //(objobjproc)Bins_contains,             /* sq_contains */
    0, //(binaryfunc)Bins_inplace_concat,       /* sq_inplace_concat */
    0 //(ssizeargfunc)Bins_inplace_repeat,      /* sq_inplace_repeat */
};



static PyObject *
Bins_items(BinsObject *self, PyObject* Py_UNUSED(ignored)){
   PyObject* items = PyDict_New();
   if (items == NULL){
        Py_RETURN_NONE;
   }
   for (int i = 0; i < self->n_bins; i++) {
        PyObject* item = self->items[i];
        if (item != NULL && item != Py_None) {
            Py_INCREF(item);
            PyObject* key = PyFloat_FromDouble((double)i*self->width);
            PyDict_SetItem(items, key, item);
        }
    }
    return items;
}

static PyObject*
Bins_props(BinsObject* self, PyObject* Py_UNUSED(ignored))
{
    PyObject* props = PyDict_New();

    PyObject* key = PyUnicode_FromString("min");
    PyObject *value = PyFloat_FromDouble((double)self->min);
    PyDict_SetItem(props, key, value);

    key = PyUnicode_FromString("max");
    value = PyFloat_FromDouble((double)self->max);
    PyDict_SetItem(props, key, value);

    key = PyUnicode_FromString("width");
    value =PyFloat_FromDouble((double)self->width);
    PyDict_SetItem(props, key, value);

    key = PyUnicode_FromString("n_bins");
    value = PyLong_FromSsize_t(self->n_bins);
    PyDict_SetItem(props, key, value);

    return props;
}

static PyObject *
Bins_reduce(BinsObject *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *tuple;
    PyObject *obj;
    PyObject *attr;
    obj = (PyObject*)self;
    attr = PyObject_GetAttrString(obj, "__class__");
    PyObject* list = PyList_New(self->n_bins);
    for (int idx = 0; idx < self->n_bins; idx++){
        if (self->items[idx] == NULL)
            PyList_SetItem(list, idx, Py_None);
        else
            PyList_SetItem(list, idx, self->items[idx]);
    }
    tuple = Py_BuildValue("O(fffiO)", attr, self->min, self->max, self->width, self->n_bins, list);
    return tuple;

}

static PyMemberDef Bins_members[] = {
	{"min", T_FLOAT, offsetof(BinsObject, min), 0, "Min bin value"},
	{"max", T_FLOAT, offsetof(BinsObject, max), 0, "Max bin value"},
	{"width", T_FLOAT, offsetof(BinsObject, width), 0, "Bin width"},
	{"n_bins", T_INT, offsetof(BinsObject, n_bins), 0, "Number of bins"},
    {NULL}  /* Sentinel */
};

static PyMethodDef Bins_methods[] = {
    {"bin", (PyCFunction)Bins_bin, METH_FASTCALL,
     "Get bin for value after binning"
    },
    {"put", (PyCFunction)Bins_put, METH_FASTCALL,
     "Put item into bin for value after binning"
    },
    {"get", (PyCFunction)Bins_get, METH_FASTCALL,
     "Get item and bin number for value after binning"
    },
    {"items", (PyCFunction)Bins_items, METH_FASTCALL,
         "Get items in bins"
    },
    {"props", (PyCFunction)Bins_props, METH_NOARGS,
         "Get Bins property-value pairs as dict"
    },
    {"__getitem__", (PyCFunction)Bins_subscript, METH_O|METH_COEXIST,
        "x.__getitem__(y) <==> x[y]"},
    {"__reduce__", (PyCFunction)Bins_reduce, METH_NOARGS,
        "Reduce Bins"
    },
    {"__sizeof__", (PyCFunction)Bins_sizeof, METH_NOARGS,
        "Sizeof Bins"
    },
	{NULL}  /* Sentinel */
};


static PyTypeObject BinsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "binstore.Bins",
    .tp_doc = "Bins objects",
	.tp_as_sequence = &Bins_as_sequence,
	.tp_as_mapping = &Bins_as_mapping,
    .tp_basicsize = sizeof(BinsObject),
    .tp_itemsize = 0,
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	.tp_new = Bins_new,
	.tp_init = (initproc)Bins_init,
    .tp_dealloc = (destructor)Bins_dealloc,
    .tp_members = Bins_members,
    .tp_methods = Bins_methods,
};

static PyModuleDef binsmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "binstore",
    .m_doc = "binstore module to implement Bins class for value-based binning of objects",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_binstore(void)
{
    PyObject* m;
    if (PyType_Ready(&BinsType) < 0)
        return NULL;

    m = PyModule_Create(&binsmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&BinsType);
    if (PyModule_AddObject(m, "Bins", (PyObject*)&BinsType) < 0) {
        Py_DECREF(&BinsType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}