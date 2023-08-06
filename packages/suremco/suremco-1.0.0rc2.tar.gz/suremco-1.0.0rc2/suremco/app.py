# SurEmCo - Main file

import time
import json
import os.path
import traceback
from argparse import ArgumentParser

from yaval import Visualizer, Values, VispyPlugin
from yaval.qt import QFileDialog

import cv2
import numpy as np
import pandas as pd

from vispy.scene import visuals
from vispy.visuals.transforms import STTransform

from .io import is_image_file, load_dataset, prepare_dataset
from .misc import Cell, to_rgb8, binarize_image, binarization_to_contours, get_subset_and_snippet, num_tokenize, \
    contour_to_mesh

try:
    from .tracker import Tracker
except ImportError:
    print("WARNING: Custom tracker not available. Was it installed correctly?")
    Tracker = None

try:
    import trackpy
except ImportError:
    print("WARNING: TrackPy not installed.")
    trackpy = None


def create_argparser():
    parser = ArgumentParser(description="SurEmCo - Superresolution Emitter Counter")

    parser.add_argument("files", metavar="files", type=str, nargs='*', default=[],
                        help="input files, one must be a DIA image")
    parser.add_argument("--disable-detection", dest="disable_detection", action='store_true')
    parser.add_argument("--drift-correction", dest="drift_correction", action='store_true')
    parser.add_argument("--show-unassigned", dest="show_unassigned", action='store_true')
    parser.add_argument("--add-cell-border", dest="border", type=float, default=0.0)
    parser.add_argument("--calibration", dest="calibration", type=float, default=0.065, help="µm per pixel")
    parser.add_argument("--keep-order", dest="keep_order", action='store_true')
    parser.add_argument("--debug", dest="debug", action='store_true', default=False)

    parser.add_argument("--process", dest="process", action='store_true')
    parser.add_argument("--parameters", dest="parameters", default=None)
    parser.add_argument("--output", dest="output", default=None)

    return parser


class SurEmCo(Visualizer):
    title = "SurEmCo - Superresolution Emitter Counter – " + \
            "by ModSim Group/IBG-1/FZ Jülich"

    result_table = True

    def visualization(self):
        parser = create_argparser()
        args = parser.parse_args()

        if len(args.files) < 2:
            args.files, _ = QFileDialog().getOpenFileNames()

            if len(args.files) == 1:
                while True:
                    new_fnames, _ = QFileDialog().getOpenFileNames()
                    if len(new_fnames) == 0:
                        break
                    else:
                        args.files += new_fnames

        average_file, tabular_files = None, []

        for filename in args.files:
            if is_image_file(filename=filename):
                average_file = filename
            else:
                tabular_files.append(filename)

        if average_file is None or tabular_files is []:
            raise SystemExit

        image = cv2.imread(average_file, -1)

        if len(image.shape) == 3:
            image = image.mean(axis=2)

        datasets = []

        maximum_frame = 0

        for tabular_file in (tabular_files if args.keep_order else sorted(tabular_files, key=num_tokenize)):
            print("Reading %s" % (tabular_file,))

            local_data = load_dataset(tabular_file)
            local_data = prepare_dataset(local_data)

            local_data.frame += maximum_frame

            datasets.append(local_data)

            maximum_frame = local_data.frame.max() + 1

        data = pd.concat(datasets)
        data.reset_index(inplace=True)
        data['original_index'] = data.index.copy()
        maximum_frame = data.frame.max()

        print("Last frame is %d" % (maximum_frame,))

        canvas = to_rgb8(image)

        if args.disable_detection:
            cells = [Cell(subset=data)]
        else:
            binarization = binarize_image(image)

            if args.debug:
                cv2.imwrite('debug_output_binarization.png', 255-(binarization * 255).astype(np.uint8))

            cells = [Cell(contour=contour) for contour in binarization_to_contours(binarization)]

            if args.debug:
                _hulls = np.zeros_like(binarization, dtype=np.uint8)

                for cell in cells:
                    cv2.drawContours(_hulls, [cell.hull], -1, 255, thickness=cv2.FILLED)

                cv2.imwrite('debug_output_hulls.png', _hulls)

                del _hulls

            # label them
            for n, cell in enumerate(cells):
                cell.name = '%d Cell' % n

            for cell in cells:
                get_subset_and_snippet(cell, data, args.border / args.calibration)

            if len(cells) == 0:
                print(
                    "WARNING: Cell detection was requested, but no cells were detected!" +
                    " Falling back to whole image as ROI"
                )

                cells = [Cell(subset=data, name='0 Everything')]

            if args.show_unassigned:
                mask = np.ones(len(data), dtype=bool)

                for cell in cells:
                    mask[cell.subset.original_index] = False

                remainder = data[mask]

                del mask

                cells.append(Cell(subset=remainder, name='%d Unassigned' % len(cells)))

                cells.append(Cell(subset=data, name='%d Everything' % len(cells)))

        if args.drift_correction:
            raise RuntimeError('Drift correction currently not implemented.')

        plugin = VispyPlugin()
        self.register_plugin(plugin)
        plugin.add_pan_zoom_camera()
        rendered_image = plugin.add_image(canvas)

        precision_label = Values.Label('precision', "Precision: %.4f µm", 0.0)
        sigma_label = Values.Label('sigma', "Sigma: %.4f µm", 0.0)

        values = [
            precision_label,
            sigma_label,
            Values.ListValue(None, [0, 1], 'live'),
            Values.ListValue(None, [cell.name for cell in cells], 'cell'),
            Values.ListValue(None, [
                'custom_moving_brute', 'custom_moving_kd', 'custom_static_brute_locprec', 'custom_static_brute_sigma',
                'custom_static_kd_locprec', 'custom_static_kd_sigma', 'trackpy'
            ], 'tracker'),
            Values.IntValue('exposure_time', 86, minimum=0, maximum=1000, unit="ms"),
            Values.IntValue('calibration', int(1000 * args.calibration), minimum=0, maximum=1000, unit="nm·pixel⁻¹"),
            Values.FloatValue('maximum_displacement', 0.195, minimum=0, maximum=20, unit="µm"),
            Values.IntValue('maximum_blink_dark', 1, minimum=0, maximum=100, unit="frame(s)"),
            Values.IntValue('image_display_frame', 0, minimum=0, maximum=maximum_frame, unit="frame"),
            Values.Action('refresh'),
            Values.Action('show_all'),
            Values.Action('analyse_all'),
            Values.Action('clear'),
            Values.Action('quit')
        ]

        if args.parameters:
            parameters = json.loads(args.parameters)
            for k, v in parameters.items():
                desired_value = next(value for value in values if value.name == k)
                desired_value.value = v

        for v in values:
            self.add_value(v)

        scatter = visuals.Markers()
        lines = visuals.Line()
        meshes = visuals.Mesh()

        plugin.view.add(scatter)
        plugin.view.add(lines)
        plugin.view.add(meshes)

        for n, cell in enumerate(cells):

            if not cell.hull.size:
                continue

            cell.contour_line = visuals.Line(pos=np.array([
                (x, y, -0.5) for x, y in cell.render_hull]),
                                             color=(0.0, 1.0, 0.0, 1.0), width=5)
            cell.contour_line_bordered = visuals.Line(pos=np.array([
                (x, y, -0.5) for x, y in cell.render_hull_bordered
            ]), color=(0.0, 0.0, 1.0, 1.0), width=5)

            plugin.view.add(cell.contour_line)
            plugin.view.add(cell.contour_line_bordered)

            center = cv2.minAreaRect(cell.hull)[0]

            cell.text = visuals.Text(text='%d' % n, color=(1, 0, 0, 1), pos=np.array((center[0], center[1], 0.5)))

            plugin.view.add(cell.text)

            cell.render_mesh = contour_to_mesh(cell.contour, 0, maximum_frame)
            # subset.frame.min(), subset.frame.max())

        result_table = [{} for _ in range(len(cells))]

        def _empty():
            for n, result in enumerate(result_table):
                result.update({
                    "Cell #": str(n),
                    "Max Displacement (µm)": float('nan'),
                    "Max Dark (frames)": float('nan'),
                    "Count": float('nan'),
                    "Mean Loc Precision (µm)": float('nan'),
                    "Mean Loc Sigma (µm)": float('nan'),
                    "Ellipse small (µm)": float('nan'),
                    "Ellipse long (µm)": float('nan'),
                    "Convex hull area (µm²)": float('nan'),
                    "Count / µm²": float('nan'),
                    "nm per pixel": 0,
                    "exposure (ms)": 0,
                    "Filename AVG": '',
                    "Filenames Results": '',
                    "Filename AVG full": '',
                    "Filenames Results full": '',
                })

            self.output_model.update_data(result_table)

        _empty()

        precision_in_pixel = data.locprec.mean()
        sigma_in_pixel = data.sigma.mean()

        def _update(values):
            micron_per_pixel = (values.calibration / 1000.0)
            # frames_per_second = 1000.0 / values.exposure_time

            precision_label.update(precision_in_pixel * micron_per_pixel)
            sigma_label.update(sigma_in_pixel * micron_per_pixel)

            def redo(n):

                cell = cells[n]
                subset = cell.subset

                before_tracking = time.time()

                tracked = None

                if values.tracker == 'trackpy' and trackpy:
                    if (
                            hasattr(cell, 'trackpy_tracked') and
                            hasattr(cell, 'trackpy_last_memory') and
                            cell.trackpy_last_memory == values.maximum_blink_dark and
                            hasattr(cell, 'trackpy_last_displacement') and
                            cell.trackpy_last_displacement == values.maximum_displacement
                    ):
                        tracked = cell.trackpy_tracked
                    else:
                        tracked = trackpy.link_df(subset, values.maximum_displacement / micron_per_pixel,
                                                  memory=values.maximum_blink_dark, link_strategy='nonrecursive')
                        cell.trackpy_last_memory = values.maximum_blink_dark
                        cell.trackpy_last_displacement = values.maximum_displacement
                        cell.trackpy_tracked = tracked
                elif values.tracker.startswith('custom') and Tracker:

                    tracker = Tracker(debug=args.debug)

                    transfer = tracker.empty_track_input_type(len(subset))

                    transfer['x'] = subset.x
                    transfer['y'] = subset.y
                    transfer['frame'] = subset.frame
                    transfer['index'] = range(len(transfer))

                    # localization precision is always the same
                    # sigma is different

                    strategy, mode, what = {
                        'custom_moving_brute': (tracker.Strategy.BRUTE_FORCE, tracker.Mode.MOVING, 'locprec'),
                        'custom_static_brute_locprec': (
                            tracker.Strategy.BRUTE_FORCE, tracker.Mode.STATIC, 'locprec'),
                        'custom_static_brute_sigma': (tracker.Strategy.BRUTE_FORCE, tracker.Mode.STATIC, 'sigma'),
                        'custom_moving_kd': (tracker.Strategy.KD_TREE, tracker.Mode.MOVING, 'locprec'),
                        'custom_static_kd_locprec': (tracker.Strategy.KD_TREE, tracker.Mode.STATIC, 'locprec'),
                        'custom_static_kd_sigma': (tracker.Strategy.KD_TREE, tracker.Mode.STATIC, 'sigma')
                    }[values.tracker]

                    if what == 'locprec':
                        transfer['precision'] = subset.locprec
                    else:
                        transfer['precision'] = subset.sigma

                    tracker.track(transfer, values.maximum_displacement / micron_per_pixel, values.maximum_blink_dark,
                                  mode, strategy)

                    tracked = subset.copy()
                    tracked['particle'] = transfer['label']
                    # expect modern pandas!
                    tracked = tracked.sort_values(by=['particle', 'frame'])

                after_tracking = time.time()

                print("Tracking took: %.2fs" % (after_tracking-before_tracking))

                # tracked

                cell.tracked = tracked

                subset = tracked
                conn = np.array(tracked.particle, dtype=np.uint32)

                nconn = np.zeros(len(conn), dtype=np.bool)

                nconn[:-1] = conn[:-1] == conn[1:]

                conn = nconn

                # subset = data

                render_data = np.c_[subset.x, subset.y, subset.frame]

                cell.render_data = render_data
                cell.render_conn = conn

                scatter.set_data(render_data, edge_color=None, face_color=(1, 1, 1, 0.5), size=5)
                lines.set_data(render_data, color=(1, 1, 1, 0.5), connect=conn)

                meshes.set_data(cell.render_mesh, color=(1, 1, 1, 0.25))

                scatter.update()
                lines.update()
                meshes.update()

                if 'Turntable' not in type(plugin.view.camera).__name__:
                    plugin.add_turntable_camera()
                    plugin.view.camera.depth_value = 1e9
                    plugin.view.camera.fov = 0.0

                result_table[n]["Max Displacement (µm)"] = values.maximum_displacement
                result_table[n]["Max Dark (frames)"] = values.maximum_blink_dark

                result_table[n]["Filename AVG"] = os.path.basename(average_file)
                result_table[n]["Filenames Results"] = "::".join(os.path.basename(t) for t in tabular_files)
                result_table[n]["Filename AVG full"] = average_file
                result_table[n]["Filenames Results full"] = "::".join(tabular_files)

                # print(tracked)
                the_count = int(tracked.particle.max())
                result_table[n]["Count"] = the_count

                result_table[n]["Mean Loc Precision (µm)"] = subset.locprec.mean() * micron_per_pixel
                result_table[n]["Mean Loc Sigma (µm)"] = subset.sigma.mean() * micron_per_pixel

                try:
                    smaller_axis = min(*cell.ellipse[1])
                    larger_axis = max(*cell.ellipse[1])
                except TypeError:
                    smaller_axis = larger_axis = 0.0

                result_table[n]["Ellipse small (µm)"] = smaller_axis * micron_per_pixel
                result_table[n]["Ellipse long (µm)"] = larger_axis * micron_per_pixel

                if len(cell.contour) > 0:
                    the_area = cv2.contourArea(cell.contour)
                    the_area *= micron_per_pixel ** 2
                    result_table[n]["Convex hull area (µm²)"] = the_area
                    result_table[n]["Count / µm²"] = the_count / the_area

                result_table[n]["exposure (ms)"] = values.exposure_time
                result_table[n]["nm per pixel"] = values.calibration

                self.output_model.update_data(result_table)

            if values['clear']:
                _empty()

            if values.quit:
                raise SystemExit

            rendered_image.transform = STTransform(translate=(0.0, 0.0, values.image_display_frame))
            rendered_image.update()

            # noinspection PyProtectedMember
            if values._modified == 'image_display_frame':
                return

            if values.refresh or values.live == 1:
                n = int(values.cell.split(' ')[0])
                try:
                    redo(n)
                except Exception as e:
                    print("A %s exception occurred in cell #%d:" % (type(e).__name__, n))
                    print(str(e))
                    traceback.print_tb(e.__traceback__)

            if values.analyse_all:  # or (values.tracker.startswith('custom') and values.live == 1):
                for n in range(len(cells)):
                    try:
                        redo(n)
                    except Exception as e:
                        print("A %s exception occurred in cell #%d:" % (type(e).__name__, n))
                        print(str(e))
                        traceback.print_tb(e.__traceback__)
                print("Done.")

                values.show_all = True

            if ('Everything' in values.cell) or ('Unassigned' in values.cell):
                values.show_all = False

            if values.show_all:

                try:

                    render_data = np.concatenate(
                        [cell.render_data for cell in cells if cell.render_data is not None])
                    # colors = np.random.random((len(render_data), 4))
                    colors = (1, 1, 1, 0.5)
                    scatter.set_data(render_data, edge_color=None, face_color=colors, size=5)
                    scatter.update()

                    render_conn = np.concatenate(
                        [cell.render_conn for cell in cells if cell.render_conn is not None])
                    lines.set_data(render_data, color=(1, 1, 1, 0.5), connect=render_conn)
                    lines.update()

                except ValueError:
                    pass

            if values.show_all or ('Everything' in values.cell) or ('Unassigned' in values.cell):
                try:
                    render_mesh = np.concatenate(
                        [cell.render_mesh for cell in cells if cell.render_mesh is not None])
                    meshes.set_data(render_mesh, color=(1, 1, 1, 0.25))
                    meshes.update()
                except ValueError:
                    pass

        if args.process:
            values = self.get_values()
            values['analyse_all'] = True
            values['_modified'] = 'analyse_all'

            print("Running analysis with parameters:")
            print(values)

            _update(values)

            print("Writing to %s" % (args.output,))

            with open(args.output, 'wt+') as fp:
                fp.write(self.output_model.get_clipboard_str())

            raise SystemExit

        return _update


def main():
    SurEmCo.run()
