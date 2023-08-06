.. _data:

Getting the Data
================

In general, you will be using `wnutils` with data you have generated with
`webnucleo <https://sourceforge.net/u/mbradle/blog>`_ codes.  However,
we have already generated some data you can use with these tutorials.
You must download those data from the web.

First, begin by creating a directory in which to work on the wnutils tutorials.
You might create this off your home directory, so you could type::

    $ cd ~
    $ mkdir wnutils_tutorials
    $ cd wnutils_tutorials

Next, download the data tarball
`wnutils_tutorials_data.tar.gz <http://nucnet-tools.sourceforge.net/data_pub/tutorials/wnutils/2018-06-09/wnutils_tutorials_data.tar.gz>`_
and move the file to your `wnutils_tutorials` directory.  Extract the
data by typing::

    $ gunzip wnutils_tutorials_data.tar.gz
    $ tar xvf wnutils_tutorials_data.tar

You can now check that you have the expected files by typing::

    $ ls

You will see the files `my_output1.h5`, `my_output2.h5`,
`my_output1.xml`, `my_output2.xml`,
and `wnutils_tutorials_data.tar`.  Since you have the data, you can remove
the tar file if you would like by typing::

    $ rm wnutils_tutorials_data.tar

You can always download that file again.

..
    Command to generate my_output.xml:

    ./single_zone_network @xml.rsp

    with xml.rsp in the sourceforge directory.

    Command to generate my_output.h5:

    ./multi_zone_network @h5.rsp  (compiled with exponential_t9_rho)

    with h5.rsp in the sourceforge directory.  Put master.h there as well.

