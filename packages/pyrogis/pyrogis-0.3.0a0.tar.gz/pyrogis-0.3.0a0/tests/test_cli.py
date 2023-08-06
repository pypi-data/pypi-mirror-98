import os
import shutil

from pyrogis.__main__ import main


def test_pyrogis_sort():
    main(args=["sort", "demo/gnome.jpg"])

    assert os.path.isfile("cooked.png")

    os.remove("cooked.png")


def test_pyrogis_sort_options():
    """
    test sort order with options
    """
    main(args=["sort", "demo/gnome.jpg", "-u", "200", "-l", "20", "-t", "2", "--ccw"])

    assert os.path.isfile("cooked.png")

    os.remove("cooked.png")


def test_pyrogis_quantize():
    main(args=["quantize", "demo/gnome.jpg"])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_quantize_options():
    """
    test quantize order with options
    """
    main(args=[
        "quantize", "demo/gnome.jpg",
        "-c", "012312", "043251",
        "-n", "4",
        "--iterations", "2",
        "--repeats", "2",
        "--initial-temp", ".8",
        "--final-temp", "0.1",
        "--dithering-level", "0.5",
    ])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_threshold():
    main(args=["threshold", "demo/gnome.jpg"])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_threshold_options():
    """
    test threshold order with options
    """
    main(args=[
        "threshold", "demo/gnome.jpg",
        "-u", "200",
        "-l", "20",
        "-i", "abaabb",
        "-e", "333433"
    ])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_resize():
    main(args=["resize", "demo/gnome.jpg"])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_resize_options():
    """
    test resize order with options
    """
    main(args=[
        "resize", "demo/gnome.jpg",
        "--width", "200",
        "--height", "300",
        "-s", "2",
        "-r", "bicubic"
    ])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_chef():
    main(args=["chef", "demo/gnome.jpg", "sort; quantize"])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")

def test_pyrogis_chef_txt():
    main(args=["chef", "demo/gnome.jpg", "demo/recipe.txt"])

    assert os.path.isfile("cooked.png")
    os.remove("cooked.png")


def test_pyrogis_plate():
    main(args=["plate", "demo/out"])

    assert os.path.isfile("cooked.gif")
    os.remove("cooked.gif")


def test_pyrogis_plate_options():
    main(args=["plate", "demo", "--fps", "25", "--duration", "20", "--no-optimize"])

    assert os.path.isfile("cooked.gif")
    os.remove("cooked.gif")


def test_pyrogis_image_with_output():
    main(args=["resize", "demo/gnome.jpg", "--output", "output.png"])

    assert os.path.isfile("output.png")
    os.remove("output.png")


def test_pyrogis_animation():
    """
    test making an animation order
    """
    main(args=["resize", "demo/octo.mp4"])

    assert len(os.listdir("cooked")) > 1
    assert os.path.isfile("cooked.gif")

    shutil.rmtree("cooked")
    os.remove("cooked.gif")


def test_pyrogis_animation_with_output_gif():
    """
    test making an animation order
    and providing an output gif filename
    """
    main(args=["resize", "demo/octo.mp4", "--output", "output.gif"])

    assert len(os.listdir("cooked")) > 1
    assert os.path.isfile("output.gif")

    shutil.rmtree("cooked")
    os.remove("output.gif")


def test_pyrogis_animation_with_output_mp4():
    """
    test making an animation order
    and providing an output gif filename
    """
    main(args=["resize", "demo/octo.mp4", "--output", "cooked.mp4"])

    assert len(os.listdir("cooked")) > 1
    assert os.path.isfile("cooked.mp4")

    shutil.rmtree("cooked")
    os.remove("cooked.mp4")


def test_pyrogis_animation_frames():
    """
    test making an animation order and not bundling the output
    """
    main(args=["resize", "demo/octo.mp4", "--frames"])

    assert len(os.listdir("cooked")) > 1
    assert not os.path.isfile("cooked.gif")

    shutil.rmtree("cooked")


def test_pyrogis_animation_frames_with_output_dir():
    """
    test making an animation order and not bundling the output
    provided an output dir
    """
    main(args=["resize", "demo/octo.mp4", "--frames", "--output", "frames"])

    assert len(os.listdir("frames")) > 1
    assert not os.path.isfile("cooked.gif")

    shutil.rmtree("frames")
