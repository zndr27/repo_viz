import dash_mantine_components as dmc
from dash_iconify import DashIconify

from natsort import natsorted
import os
from pathlib import Path


class FileTree:

    def __init__(self, filepath: os.PathLike):
        """
        Usage: component = FileTree('Path/to/my/File').render()
        """
        self.filepath = filepath

    def render(self) -> dmc.Accordion:
        return dmc.Accordion(
            self.build_tree(self.filepath, isRoot=True),
            multiple=True,
        )

    def flatten(self, l):
        return [item for sublist in l for item in sublist]

    def make_file(self, file_name):
        return dmc.Text(
            [DashIconify(icon="akar-icons:file"), " ", file_name],
            style={"paddingTop": "5px"},
        )

    def make_folder(self, folder_name):
        # return [DashIconify(icon="akar-icons:folder"), " ", folder_name]
        return dmc.Text([DashIconify(icon="akar-icons:folder"), " ", folder_name])

    def build_tree(self, path, isRoot=False):
        d = []
        if os.path.isdir(path):
            list_dir = natsorted([x for x in Path(path).iterdir() if x.is_dir()])
            list_dir += natsorted([x for x in Path(path).iterdir() if not x.is_dir()])

            children = self.flatten(
                [self.build_tree(os.path.join(path, x)) for x in list_dir]
            )
            if isRoot:
                d.append(
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(
                                self.make_folder(os.path.basename(path))
                            ),
                            dmc.AccordionPanel(children=children),
                        ],
                        value=str(path),
                    )
                )
            else:
                d.append(
                    dmc.Accordion(
                        [
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(
                                        self.make_folder(os.path.basename(path))
                                    ),
                                    dmc.AccordionPanel(children=children),
                                ],
                                value=str(path),
                            )
                        ],
                        multiple=True,
                    )
                )
        else:
            d.append(self.make_file(os.path.basename(path)))
        return d
