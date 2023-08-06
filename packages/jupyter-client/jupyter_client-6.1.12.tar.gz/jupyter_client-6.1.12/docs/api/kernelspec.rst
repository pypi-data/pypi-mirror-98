kernelspec - discovering kernels
================================

.. seealso:: :ref:`kernelspecs`

.. module:: jupyter_client.kernelspec

.. class:: KernelSpec

   .. attribute:: argv

      The list of arguments to start this kernel.

   .. attribute:: env

      A dictionary of extra environment variables to declare, in addition to
      the current environment variables, when launching this kernel.

   .. attribute:: display_name

      The name to display for this kernel in UI.

   .. attribute:: language

      The name of the language the kernel implements, to help with picking
      appropriate kernels when loading notebooks.

   .. attribute:: metadata

      Additional kernel-specific metadata; clients can use this as needed,
      for instance to aid in kernel selection and filtering.

      Metadata added here should be namespaced for the tool reading and
      writing that metadata. Concretely, if you're adding a new field called
      :code:`supported_versions` which your tool recognizes, then you should
      add it as :code:`"mytool": {"supported_versions": [1, 2]}`, **not** as a
      top-level field called :code:`supported_versions`.

   .. attribute:: resource_dir

      The path to the directory with this kernel's resources, such as icons.

   .. automethod:: to_json

.. class:: KernelSpecManager

   .. automethod:: find_kernel_specs

   .. automethod:: get_all_specs

   .. automethod:: get_kernel_spec

   .. automethod:: install_kernel_spec

.. exception:: NoSuchKernel

   .. attribute:: name

      The name of the kernel which was requested.

.. function:: find_kernel_specs
              get_kernel_spec(kernel_name)
              install_kernel_spec(source_dir, kernel_name=None, user=False, replace=False)

   These methods from :class:`KernelSpecManager` are exposed as functions on the
   module as well; they will use all the default settings.
