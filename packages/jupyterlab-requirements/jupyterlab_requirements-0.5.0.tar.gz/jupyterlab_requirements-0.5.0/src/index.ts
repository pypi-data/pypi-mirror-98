/**
 * Jupyterlab requirements.
 *
 * Jupyterlab extension for managing dependencies.
 *
 * @link   https://github.com/thoth-station/jupyterlab-requirements#readme
 * @file   Jupyterlab extension for managing dependencies.
 * @author Francesco Murdaca <fmurdaca@redhat.com>
 * @since  0.0.1
 */

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';


// Customizations
import { ManageDependenciesButtonExtension } from './dependencyManagementButton';

/**
 * The command IDs used by the console plugin.
 */
 export const commandIDs = {
  dependencyManagement: 'notebook:manage-dependencies',
};

/**
 * Initialization data for the jupyterlab_requirements extension.
 */

const extension: JupyterFrontEndPlugin<string> = {
  id: 'jupyterlab_requirements',
  autoStart: true,
  activate
};

/**
 * Activate the JupyterLab extension.
 *
 * @param app Jupyter Front End
 */

async function activate (
  app: JupyterFrontEnd,
): Promise<string> {

  // Add button in notebook menu
  try {
    // ManageDependenciesButtonExtension initialization code
    const buttonExtension = new ManageDependenciesButtonExtension();
    app.docRegistry.addWidgetExtension('Notebook', buttonExtension);
    console.log('jupyterlab-requirements extension is activated!');
  } catch (reason) {
    console.error('Error on setting the jupyterlab-requirements extension');
  }

  return "ready"
}

export default extension;
