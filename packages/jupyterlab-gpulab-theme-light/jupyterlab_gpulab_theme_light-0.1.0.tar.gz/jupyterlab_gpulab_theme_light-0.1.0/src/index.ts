import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_gpulab_theme_light extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_gpulab_theme_light',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log(
      'JupyterLab extension jupyterlab_gpulab_theme_light is activated!'
    );
    const style = 'jupyterlab_gpulab_theme_light/index.css';

    manager.register({
      name: 'GPULab Light',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default extension;
