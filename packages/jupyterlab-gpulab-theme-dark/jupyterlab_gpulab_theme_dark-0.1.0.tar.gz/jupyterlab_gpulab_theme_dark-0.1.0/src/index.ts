import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_gpulab_theme_dark extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_gpulab_theme_dark',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log(
      'JupyterLab extension jupyterlab_gpulab_theme_dark is activated!'
    );
    const style = 'jupyterlab_gpulab_theme_dark/index.css';

    manager.register({
      name: 'GPULab Dark',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default extension;
