####################################
Qiskit Metal |version| documentation
####################################

.. hint::
    
    You can open this documentation using

    .. code-block:: python

        import qiskit_metal
        qiskit_metal.open_docs()

.. attention::
    
    This is an early-access alpha version of Qiskit Metal. This folder will be expanded throughout the early-access period, based on both planned training and your feedback. Please let us know about anything you might want us to add or elaborate upon. 


| **Qiskit for quantum hardware design (`Qiskit Metal`)** is a quantum device design and analysis SDK, library, and community.
| Call it quantum EDA (QEDA) and analysis. 


.. rubric:: About Metal

Designing quantum devices is the bedrock of the quantum ecosystem, but it is a difficult, multi-step process that connects traditionally disparate worlds.

Metal is automating and streamlining this process. Our vision is to develop a community-driven universal platform capable of orchestrating quantum chip development from concept to fabrication in a simple and open framework.
Qiskit for quantum hardware design (`Qiskit Metal`) is:
* Open source
* Community-driven
* Both a python API and a front-end visual GUI interface.

.. rubric:: Metal & it's vision (read full `Medium blog <https://medium.com/qiskit/what-if-we-had-a-computer-aided-design-program-for-quantum-computers-4cb88bd1ddea>`_):

.. highlights::

    We want to accelerate and lower the barrier to innovation on quantum devices. 
    Today at the IEEE Quantum Week Conference, the team discussed their vision for this first-of-its-kind project. Led by quantum physicist Zlatko Minev and 
    developed with other IBM Quantum team members, this project is meant for those interested in quantum hardware design: a suite of design automation 
    tools that can be used to devise and analyze superconducting devices, with a focus on being able to integrate the best tools into a quantum hardware 
    designer’s workflow. We’ve code-named the project Qiskit Metal.

    We hope that as a community, we might make the process of quantization — bridging the gap between pieces of a superconducting metal on a quantum chip 
    with the computational mathematics of Hamiltonians and Hilbert spaces — available to anyone with a curious mind and a laptop. We want to make quantum 
    device design a streamlined process that automates the laborious tasks as it does with conventional electronic device design. We are writing software
    with built-in best practices and cutting-edge quantum analysis techniques, all this while seamlessly leveraging the power of conventional EDA tools. 
    The goal of Qiskit Metal is to allow for easy quantum hardware modeling with reduction of design-related errors plus increased speed.

**Qiskit Metal consists of four foundational elements:**

    - :ref:`Quantum Device Design (QDesign)<todo>`: ...
    - :ref:`Quantum Device Components (QComponent)<todo>`: ...
    - :ref:`Quantum Renderer (QRenderer)<todo>`: ...
    - :ref:`Quantum Analysis (QAnalysis)<todo>`: ...

.. toctree::
    :maxdepth: 2
    :hidden:

    Metal Workflow<workflow>
    Frequently Asked Questions<faq>

.. TODO: Add Installing Qiskit Metal<getting_started/install.rst> before Metal Workflow
.. TODO: Add Getting Started With Metal between Metal Workflow and Installing Qiskit Metal

.. toctree::
    :maxdepth: 2
    :caption: Contributor Guide
    :hidden:

    Contributor Guide<contributor-guide>


.. toctree::
    :maxdepth: 2
    :caption: Tutorials
    :hidden:

.. TODO: Add jupyter notebooks here

.. toctree::
    :maxdepth: 2
    :caption: Libraries
    :hidden:

    Quantum devices<apidocs/qlibrary>

.. toctree::
    :maxdepth: 2
    :caption: API References
    :hidden:

    Overview<overview>
    QDesign<apidocs/designs>
    Analyse<apidocs/analyses>
    Renderer<apidocs/renderers>
    Toolbox<apidocs/toolbox_metal>
  
.. toctree::
    :maxdepth: 2
    :caption: API References Advanced
    :hidden:

    GUI<apidocs/gui>
    QGeometry Tables<apidocs/qgeometries>


.. Hiding - Indices and tables
   :ref:`genindex`
   :ref:`modindex`
   :ref:`search`
