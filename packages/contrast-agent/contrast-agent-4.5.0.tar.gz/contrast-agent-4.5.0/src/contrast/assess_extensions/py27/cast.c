/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>


#define IS_TRACKABLE(X) (       \
        PyUnicode_Check((X)) || \
        PyBytes_Check((X)) ||  \
        PyByteArray_Check((X)))


newfunc unicode_new_orig;
PyObject *(*from_encoded_object_orig)(register PyObject *, const char *, const char *);
PyObject *(*object_unicode_orig)(PyObject *);


// Propagate for the case where non-string object is explicitly converted to unicode
// This will handle any propagation within the __str__ method of arbitrary objects when
// converting to str/unicode.
PyObject *from_encoded_object_new(register PyObject* obj, const char *encoding, const char *errors) {
    PyObject *result;
    PyObject *args;

    enter_propagation_scope();
    result = from_encoded_object_orig(obj, encoding, errors);
    exit_propagation_scope();

    if (result == NULL)
        return result;

    args = PyTuple_Pack(1, obj);
    propagate_result("CAST", NULL, result, args, NULL);

    Py_XDECREF(args);
    return result;
}


// Hook for propagation through explicit casts to unicode type
PyObject *unicode_new_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *t = NULL;
    PyObject *result;

    if (args != NULL) {
        t = PyTuple_GetItem(args, 0); // borrowed reference
    }

    if (t == NULL) {
        PyErr_Clear();

        if (kwds != NULL) {
            // If args are not present, there might be a kwarg instead
            // This function returns NULL and does *NOT* set an error if the key is not
            // found. It returns a borrowed reference otherwise.
            t = PyDict_GetItemString(kwds, "string");
        }
    }

    // If the given parameter type is not something we can track, simply return without
    // propagation. If we need to propagate for __str__, it will be handled by a
    // different hook.
    if (type == &PyUnicode_Type && (t == NULL || !IS_TRACKABLE(t))) {
        return unicode_new_orig(type, args, kwds);
    }

    // Enter scope here in order to avoid creating multiple events in case the original
    // function ends up causing other hooked propagators to be called.
    enter_propagation_scope();
    result = unicode_new_orig(type, args, kwds);
    exit_propagation_scope();

    if (result != NULL)
        propagate_result("CAST", NULL, result, args, kwds);

    return result;

}


int apply_cast_patches(funchook_t *funchook) {
    ADD_NEWFUNC_HOOK(PyUnicode_Type, unicode_new);

    from_encoded_object_orig = PyUnicode_FromEncodedObject;
    funchook_prep_wrapper(funchook, &from_encoded_object_orig, from_encoded_object_new);

    return 0;
}
