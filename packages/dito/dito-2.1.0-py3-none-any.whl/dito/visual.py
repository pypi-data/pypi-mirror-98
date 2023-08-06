import os.path

import cv2
import numpy as np

import dito.core
import dito.data
import dito.io
import dito.utils


def get_colormap(name):
    """
    Returns the colormap specified by `name` as `uint8` NumPy array of size
    `(256, 1, 3)`.
    """
    
    # source 1: non-OpenCV colormaps
    data_key = "colormap:{}".format(name.lower())
    if data_key in dito.data.RESOURCES_FILENAMES.keys():
        return dito.io.load(filename=dito.data.RESOURCES_FILENAMES[data_key])
    
    # source 2: OpenCV colormaps
    full_cv2_name = "COLORMAP_{}".format(name.upper())
    if hasattr(cv2, full_cv2_name):
        return cv2.applyColorMap(src=dito.data.yslope(width=1), colormap=getattr(cv2, full_cv2_name))
    
    # no match
    raise ValueError("Unknown colormap '{}'".format(name))


def is_colormap(colormap):
    """
    Returns `True` iff `colormap` is a OpenCV-compatible colormap.
    
    For this, `colormap` must be a `uint8` array of shape `(256, 1, 3)`, i.e.
    a color image of size `1x256`.
    """
    if not dito.core.is_image(image=colormap):
        return False
    if colormap.dtype != np.uint8:
        return False
    if colormap.shape != (256, 1, 3):
        return False
    return True


def colorize(image, colormap):
    """
    Colorize the `image` using the colormap identified by `colormap_name`.
    """
    if isinstance(colormap, str):
        return cv2.applyColorMap(src=image, userColor=get_colormap(name=colormap))
    elif is_colormap(colormap=colormap):
        return cv2.applyColorMap(src=image, userColor=colormap)
    else:
        raise TypeError("Argument `colormap` must either be a string (the colormap name) or a valid colormap.")


####
#%%% image stacking
####


def stack(images, padding=0, background_color=0, dtype=None, gray=None):
    """
    Stack given images into one image.

    `images` must be a vector of images (in which case the images are stacked
    horizontally) or a vector of vectors of images, defining rows and columns.
    """

    # check argument `images`
    if isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], np.ndarray):
        # `images` is a vector of images
        rows = [images]
    elif isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], (tuple, list)) and (len(images[0]) > 0) and isinstance(images[0][0], np.ndarray):
        # `images` is a vector of vectors of images
        rows = images
    else:
        raise ValueError("Invalid argument 'images' - must be vector of images or vector of vectors of images")

    # find common data type and color mode
    if dtype is None:
        dtype = dito.core.dtype_common((image.dtype for row in rows for image in row))
    if gray is None:
        gray = all(dito.core.is_gray(image=image) for row in rows for image in row)

    # step 1/2: construct stacked image for each row
    row_images = []
    width = 0
    for (n_row, row) in enumerate(rows):
        # determine row height
        row_height = 0
        for image in row:
            row_height = max(row_height, image.shape[0])
        if n_row == 0:
            row_height += 2 * padding
        else:
            row_height += padding

        # construct image
        row_image = None
        for (n_col, image) in enumerate(row):
            # convert individual image to target data type and color mode
            image = dito.core.convert(image=image, dtype=dtype)
            if gray:
                image = dito.core.as_gray(image=image)
            else:
                image = dito.core.as_color(image=image)

            # add padding
            pad_width = [[padding if n_row == 0 else 0, padding], [padding if n_col == 0 else 0, padding]]
            if not gray:
                pad_width.append([0, 0])
            image = np.pad(array=image, pad_width=pad_width, mode="constant", constant_values=background_color)

            # ensure that image has the height of the row
            gap = row_height - image.shape[0]
            if gap > 0:
                if gray:
                    image_fill = np.zeros(shape=(gap, image.shape[1]), dtype=dtype) + background_color
                else:
                    image_fill = np.zeros(shape=(gap, image.shape[1], 3), dtype=dtype) + background_color
                image = np.vstack(tup=(image, image_fill))

            # add to current row image
            if row_image is None:
                row_image = image
            else:
                row_image = np.hstack(tup=(row_image, image))

        # update max width
        width = max(width, row_image.shape[1])
        row_images.append(row_image)

    # step 2/2: construct stacked image from the row images
    stacked_image = None
    for row_image in row_images:
        # ensure that the row image has the width of the final image
        gap = width - row_image.shape[1]
        if gap > 0:
            if gray:
                image_fill = np.zeros(shape=(row_image.shape[0], gap), dtype=dtype) + background_color
            else:
                image_fill = np.zeros(shape=(row_image.shape[0], gap, 3), dtype=dtype) + background_color
            row_image = np.hstack(tup=(row_image, image_fill))

        # add to final image
        if stacked_image is None:
            stacked_image = row_image
        else:
            stacked_image = np.vstack(tup=(stacked_image, row_image))

    return stacked_image


####
#%%% text
####


def text(image, message, position=(0.0, 0.0), anchor="lt", font="sans", scale=1.0, thickness=1, padding_rel=1.0, inner_color=(255, 255, 255), outer_color=None, background_color=0, line_type=cv2.LINE_AA):
    """
    Draws the text `message` into the given `image`.

    The `position` is given as 2D point in relative coordinates (i.e., with
    coordinate ranges of [0.0, 1.0]). The `anchor` must be given as two letter
    string, following the pattern `[lcr][tcb]`. It specifies the horizontal
    and vertical alignment of the text with respect to the given position. The
    `padding_rel` is given in (possibly non-integer) multiples of the font's
    baseline height.
    """

    # keep input image unchanged
    image = image.copy()

    # font
    if font == "sans":
        font_face = cv2.FONT_HERSHEY_DUPLEX
    elif font == "serif":
        font_face = cv2.FONT_HERSHEY_TRIPLEX
    else:
        raise ValueError("Invalid font '{}'".format(font))
    font_scale = scale
    font_thickness = thickness

    # calculate width and height of the text
    ((text_width, text_height), baseline) = cv2.getTextSize(
        text=message,
        fontFace=font_face,
        fontScale=font_scale,
        thickness=font_thickness,
    )

    # base offset derived from the specified position
    offset = np.array([
        position[0] * image.shape[1],
        position[1] * (image.shape[0] - baseline),
    ])

    # adjust offset based on the specified anchor type
    if not (isinstance(anchor, str) and (len(anchor) == 2) and (anchor[0] in ("l", "c", "r")) and (anchor[1] in ("t", "c", "b"))):
        raise ValueError("Argument 'anchor' must be a string of length two (pattern: '[lcr][tcb]') , but is '{}'".format(anchor))
    (anchor_h, anchor_v) = anchor
    if anchor_h == "l":
        pass
    elif anchor_h == "c":
        offset[0] -= text_width * 0.5
    elif anchor_h == "r":
        offset[0] -= text_width
    if anchor_v == "t":
        offset[1] += text_height
    elif anchor_v == "c":
        offset[1] += text_height * 0.5
    elif anchor_v == "b":
        pass

    # finalize offset
    offset = dito.core.tir(*offset)

    # add padding to offset
    padding_abs = round(padding_rel * baseline)

    # draw background rectangle
    if background_color is not None:
        # TODO: allow actual BGR color, not just one intensity value (use cv2.rectangle for drawing)
        image[max(0, offset[1] - text_height - padding_abs):min(image.shape[0], offset[1] + max(baseline, padding_abs)), max(0, offset[0] - padding_abs):min(image.shape[1], offset[0] + text_width + padding_abs), ...] = background_color

    # draw text
    if outer_color is not None:
        cv2.putText(
            img=image,
            text=message,
            org=offset,
            fontFace=font_face,
            fontScale=font_scale,
            color=outer_color,
            thickness=font_thickness + 2,
            lineType=line_type,
            bottomLeftOrigin=False,
        )
    cv2.putText(
        img=image,
        text=message,
        org=offset,
        fontFace=font_face,
        fontScale=font_scale,
        color=inner_color,
        thickness=font_thickness,
        lineType=line_type,
        bottomLeftOrigin=False,
    )

    return image


####
#%%% image visualization
####


def get_screenres(fallback=(1920, 1080)):
    """
    Return the resolution (width, height) of the screen in pixels.

    If it can not be determined, assume 1920x1080.
    See http://stackoverflow.com/a/3949983 for info.
    """



    try:
        import tkinter as tk
    except ImportError:
        return fallback

    try:
        root = tk.Tk()
    except tk.TclError:
        return fallback
    (width, height) = (root.winfo_screenwidth(), root.winfo_screenheight())
    root.destroy()
    return (width, height)


def qkeys():
    """
    Returns a tuple of key codes ('unicode code points', as returned by
    `ord()` which correspond to key presses indicating the desire to
    quit (`<ESC>`, `q`).

    >>> qkeys()
    (27, 113)
    """

    return (27, ord("q"))


def prepare_for_display(image, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None):
    """
    Prepare `image` (or a list or a list of lists of images) for being
    displayed on the screen (or similar purposes).

    Internal function used by `show` and `MultiShow`.
    """
    if isinstance(image, np.ndarray):
        # use image as is
        pass
    elif isinstance(image, (list, tuple)) and (len(image) > 0) and isinstance(image[0], np.ndarray):
        # list of images: stack them into one image
        image = stack(images=[image])
    elif isinstance(image, (list, tuple)) and (len(image) > 0) and isinstance(image[0], (list, tuple)) and (len(image[0]) > 0) and isinstance(image[0][0], np.ndarray):
        # list of lists of images: stack them into one image
        image = stack(images=image)
    else:
        raise ValueError("Invalid value for parameter `image` ({}) - it must either be (i) an image, (ii) a non-empty list of images or a non-empty list of non-empty lists of images".format(image))

    # normalize intensity values
    if normalize_mode is not None:
        image = dito.core.normalize(image=image, mode=normalize_mode, **normalize_kwargs)

    # resize image
    if scale is None:
        # try to find a good scale factor automatically
        (width, height) = get_screenres()
        scale = 0.85 * min(height / image.shape[0], width / image.shape[1])
    image = dito.core.resize(image=image, scale_or_size=scale)

    # apply colormap
    if colormap is not None:
        image = colorize(image=image, colormap=colormap)

    return image


def show(image, wait=0, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None, window_name="dito.show", close_window=False, engine=None):
    """
    Show `image` on the screen.

    If `image` is a list of images or a list of lists of images, they are
    stacked into one image.
    """

    image_show = prepare_for_display(image=image, scale=scale, normalize_mode=normalize_mode, normalize_kwargs=normalize_kwargs, colormap=colormap)

    # determine how to display the image
    if engine is None:
        # TODO: auto-detect if in notebook
        engine = "cv2"

    # show
    if engine == "cv2":
        try:
            cv2.imshow(window_name, image_show)
            key = cv2.waitKey(wait)
        finally:
            if close_window:
                cv2.destroyWindow(window_name)

    elif engine == "ipython":
        # source: https://gist.github.com/uduse/e3122b708a8871dfe9643908e6ef5c54
        import io
        import IPython.display
        import PIL.Image
        f = io.BytesIO()
        # TODO: this just encodes the image array as PNG bytes - we don't need PIL for that -> remove PIL
        PIL.Image.fromarray(image).save(f, "png")
        IPython.display.display(IPython.display.Image(data=f.getvalue()))
        key = -1

    else:
        raise RuntimeError("Unsupported engine '{}'".format(engine))

    return key


class MultiShow():
    """
    Extension of the functionality provided by the `dito.show` function.

    It keeps all images that have been shown and can re-show them interactively.
    """
    def __init__(self, window_name="dito.MultiShow", close_window=False, save_dir=None):
        self.window_name = window_name
        self.close_window = close_window
        self.save_dir = save_dir
        self.engine = "cv2"
        self.images = []

    def save(self, n_image):
        if self.save_dir is None:
            self.save_dir = dito.utils.get_temp_dir(prefix="dito.MultiShow.{}.".format(dito.utils.now_str())).name
        filename = os.path.join(self.save_dir, "{:>08d}.png".format(n_image + 1))
        dito.io.save(filename=filename, image=self.images[n_image])
        print("Saved image {}/{} to file '{}'".format(n_image + 1, len(self.images), filename))

    def save_all(self):
        for n_image in range(len(self.images)):
            self.save(n_image=n_image)

    def _show(self, image, wait):
        """
        Internal method used to actually show an image on the screen.
        """
        return show(image=image, wait=wait, scale=1.0, normalize_mode=None, normalize_kwargs=dict(), colormap=None, window_name=self.window_name, close_window=self.close_window, engine=self.engine)

    def show(self, image, wait=0, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None, keep=True, hide=False):
        """
        Shows image on the screen, just as `dito.show` would. However, the
        image is also stored internally, and can be re-shown anytime.
        """
        image_show = prepare_for_display(image=image, scale=scale, normalize_mode=normalize_mode, normalize_kwargs=normalize_kwargs, colormap=colormap)
        if keep:
            self.images.append(image_show)
        if not hide:
            return self._show(image=image_show, wait=wait)
        else:
            return -1

    def reshow(self, n_image, wait=0):
        """
        Re-show specific image.
        """
        return self._show(image=self.images[n_image], wait=wait)

    def reshow_interactive(self):
        """
        Re-show all images interactively.
        """
        image_count = len(self.images)
        if image_count == 0:
            raise RuntimeError("No images available")

        # initial settings
        n_image = image_count - 1
        show_overlay = True

        # start loop
        while True:
            # get image to show
            image = self.images[n_image]
            if show_overlay:
                image = text(image=image, message="{}/{}".format(n_image + 1, image_count), scale=0.5)

            # show image
            key = self._show(image=image, wait=0)

            # handle keys
            if key in (ord("+"),):
                # show next image
                n_image = (n_image + 1) % image_count
            elif key in (ord("-"),):
                # show previous image
                n_image = (n_image - 1) % image_count
            elif key in (ord(" "),):
                # toggle overlay
                show_overlay = not show_overlay
            elif key in (ord("s"),):
                # save current image
                self.save(n_image=n_image)
            elif key in (ord("a"),):
                # save all images
                self.save_all()
            elif key in qkeys():
                # quit
                break

            if self.close_window:
                cv2.destroyWindow(winname=self.window_name)
