from dj_notebook import activate
from dj_notebook.shell_plus import DiagramClass


def test_thing():
    plus = activate("test_harness")
    # TODO capture STDOUT and assert on it
    assert plus.print() is None


def test_namify():
    """
    Test the `namify` method of the `DiagramClass`.

    Checks if the `namify` method correctly converts the class
    name and its module into a format that replaces dots with underscores.
    Test covers three scenarios:
    1. Built-in classes (e.g., `str`).
    2. Custom classes (e.g., `DiagramClass`).
    3. Nested classes (e.g., `OuterClass.InnerClass`).

    TODO: Maybe add scenarios of periods included in naming to
    test conversion
    """
    # Create an instance of DiagramClass - include a sample class
    diagram = DiagramClass(str)

    # Test built-in class
    assert diagram.namify(str) == "builtins_str"

    # Test custom class
    assert diagram.namify(DiagramClass) == "dj_notebook_shell_plus_DiagramClass"

    # Test nested class
    class OuterClass:
        class InnerClass:
            pass

    assert diagram.namify(OuterClass.InnerClass) == "tests_test_dj_notebook_InnerClass"


def test_draw_connections():
    """
    Test the `draw_connections` functionality of the `DiagramClass`.

    Verifies that the graph generated by `DiagramClass` correctly
    reflects the relationships between a sample class (`SampleClass`) and its
    direct base classes (`TestClassA` and `TestClassB`).

    TODO: There is an oddity with needing to add 2 leading spaces to the
    assertions... look on line 47 in the `draw_connections` definition
    which it needs to match.
    """

    # Define base classes
    class TestClassA:
        pass

    class TestClassB:
        pass

    # Create a sample class that inherits from the base classes
    class SampleClass(TestClassA, TestClassB):
        pass

    diagram = DiagramClass(SampleClass)

    # Check if the graph has nodes for the SampleClass and its ancestors
    sample_class_node = (
        f"  class {diagram.namify(SampleClass)}"
        f'["{SampleClass.__module__}::{SampleClass.__name__}"]'
    )
    assert sample_class_node in diagram.graph

    test_class_a_node = (
        f"  class {diagram.namify(TestClassA)}"
        f'["{TestClassA.__module__}::{TestClassA.__name__}"]'
    )
    assert test_class_a_node in diagram.graph

    test_class_b_node = (
        f"  class {diagram.namify(TestClassB)}"
        f'["{TestClassB.__module__}::{TestClassB.__name__}"]'
    )
    assert test_class_b_node in diagram.graph

    # Check if the graph has connections between the SampleClass and its ancestors
    assert (
        f"  {diagram.namify(TestClassA)} <|-- {diagram.namify(SampleClass)}"
        in diagram.graph
    )
    assert (
        f"  {diagram.namify(TestClassB)} <|-- {diagram.namify(SampleClass)}"
        in diagram.graph
    )
