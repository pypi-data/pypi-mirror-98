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

import _ from "lodash";

import * as React from 'react';

import { NotebookPanel } from '@jupyterlab/notebook';

import { DependencyManagementForm } from './dependencyManagementForm'
import { DependencyManagementSaveButton } from './dependencyManagementSaveButton'
import { DependencyManagementInstallButton } from './dependencyManagementInstallButton'
import { DependencyManagementNewPackageButton } from './dependencyManagementAddPackageButton';

import { get_python_version, take_notebook_content } from "../notebook";
import { Requirements, RequirementsLock } from '../types/requirements';

import { ThothConfig } from '../types/thoth';

import {
  install_packages,
  create_new_kernel
} from '../kernel';

import {
  update_thoth_config_on_disk,
  lock_requirements_with_thoth,
  lock_requirements_with_pipenv
} from '../thoth';

import {
  get_kernel_name
} from "../notebook"

import { KernelModel } from '../model';

import { Advise } from "../types/thoth";

import {
  parse_inputs_from_metadata,
  set_notebook_metadata,
  store_dependencies_on_disk,
  _parse_packages_from_state,
  _handle_deleted_packages_case,
  _handle_total_packages_case
} from "../helpers";

/**
 * The class name added to the new package button (CSS).
 */
const OK_BUTTON_CLASS = "thoth-ok-button";
const THOTH_KERNEL_NAME_INPUT = "thoth-kernel-name-input";
const CONTAINER_BUTTON = "thoth-container-button";
const CONTAINER_BUTTON_CENTRE = "thoth-container-button-centre";

/**
 * Class: Holds properties for DependenciesManagementDialog.
 */

export interface IDependencyManagementUIProps {
  panel: NotebookPanel
  loaded_requirements: Requirements,
  loaded_requirements_lock: RequirementsLock,
  loaded_config_file: ThothConfig,
  loaded_resolution_engine: string
}

/**
 * Class: Holds state for DependenciesManagementDialog.
 */

export interface IDependencyManagementUIState {
  kernel_name: string
  recommendation_type: string
  status: string,
  packages: { [ name: string ]: string },
  installed_packages: { [ name: string ]: string },
  loaded_packages: { [ name: string ]: string },
  deleted_packages: { [ name: string ]: string },
  requirements: Requirements,
  thoth_config: ThothConfig,
  error_msg: string,
  resolution_engine: string
}

/**
 * A React Component for handling dependency management.
 */

export class DependenciesManagementUI extends React.Component<IDependencyManagementUIProps, IDependencyManagementUIState> {
    constructor(
      props: IDependencyManagementUIProps
    ) {
      super(props);

      this.onStart = this.onStart.bind(this),
      this.execute_code_in_kernel = this.execute_code_in_kernel.bind(this),
      this.changeUIstate = this.changeUIstate.bind(this),
      this.addNewRow = this.addNewRow.bind(this),
      this.editRow = this.editRow.bind(this),
      this.editSavedRow = this.editSavedRow.bind(this),
      this.storeRow = this.storeRow.bind(this),
      this.deleteRow = this.deleteRow.bind(this),
      this.deleteSavedRow = this.deleteSavedRow.bind(this),
      this.onSave = this.onSave.bind(this),
      this.lock_using_thoth = this.lock_using_thoth.bind(this),
      this.lock_using_pipenv = this.lock_using_pipenv.bind(this),
      this.install = this.install.bind(this),
      this.setKernel = this.setKernel.bind(this),
      this.setKernelName = this.setKernelName.bind(this)
      this.setRecommendationType = this.setRecommendationType.bind(this)

      this._model = new KernelModel ( this.props.panel.sessionContext )

      this.state = {
        kernel_name: get_kernel_name( this.props.panel ),
        recommendation_type: "latest",
        status: "loading",
        packages: {},  // editing
        loaded_packages: {},
        installed_packages: {},
        deleted_packages: {},
        requirements: {
          packages: {},
          requires: { python_version: get_python_version( this.props.panel ) },
          sources: [{
            name: "pypi",
            url: "https://pypi.org/simple",
            verify_ssl: true,
          }]
        },
        thoth_config: {
          host: "khemenu.thoth-station.ninja",
          tls_verify: false,
          requirements_format: "pipenv",
          runtime_environments: [{
            name: "ubi:8",
            operating_system: {
              name: "ubi",
              version: "8",
            },
            python_version: "3.8",
            recommendation_type: "latest"
        }]
        },
        error_msg: undefined,
        resolution_engine: "thoth"
      }
    }

    /**
     * Function to execute code in the kernel as a cell in the notebook
     */

    async execute_code_in_kernel(code: string) {
      await this._model.execute( code )
    }


    /**
     * Function: Main function to change state and status!
     */

    changeUIstate(
      status: string,
      packages: { [ name: string ]: string },
      loaded_packages: { [ name: string ]: string },
      installed_packages: { [ name: string ]: string },
      deleted_packages: { [ name: string ]: string },
      requirements: Requirements,
      kernel_name: string,
      thoth_config: ThothConfig,
      error_msg?: string,
    ) {

      var new_state: IDependencyManagementUIState = this.state
      console.debug("initial", new_state)

      _.set(new_state, "status", status)

      _.set(new_state, "packages", packages)

      _.set(new_state, "loaded_packages", loaded_packages)

      _.set(new_state, "installed_packages", installed_packages)

      _.set(new_state, "deleted_packages", deleted_packages)

      _.set(new_state, "requirements", requirements)

      _.set(new_state, "kernel_name", kernel_name)

      _.set(new_state, "thoth_config", thoth_config)

      _.set(new_state, "error_msg", error_msg)

      console.debug("new", new_state)
      this.setState(new_state);
    }

    /**
     * Function: Set recommendation type for thamos advise
     */

    setRecommendationType(recommendation_type: string) {

      this.setState(
        {
          recommendation_type: recommendation_type
        }
      );

    }

    /**
     * Function: Set recommendation type for thamos advise
     */

    async setNewState(ui_state: IDependencyManagementUIState) {

      console.log("new state", ui_state)
      this.setState(ui_state);
    }

    changeRecommendationType(event: React .ChangeEvent<HTMLInputElement>) {

        const recommendation_type = event.target.value;
        this.setRecommendationType( recommendation_type )
  }

    /**
     * Function: Set Kernel name to be created and assigned to notebook
     */

    setKernelName(event: React.ChangeEvent<HTMLInputElement>) {

      const kernel_name = event.target.value

      this.setState(
        {
          kernel_name: kernel_name
        }
      );

    }

    /**
     * Function: Add new empty row (Only one can be added at the time)
     */

    addNewRow() {

      const packages = this.state.packages

      _.set(packages, "", "")
      console.debug("added package", packages)

      this.changeUIstate(
        "editing",
        packages,
        this.state.loaded_packages,
        this.state.installed_packages,
        this.state.deleted_packages,
        this.state.requirements,
        this.state.kernel_name,
        this.state.thoth_config
      )
    }

    /**
     * Function: Edit added row
     */

    editRow(package_name: string) {

      const packages = this.state.packages

      _.unset(packages, package_name)
      _.set(packages, "", "*")

      console.debug("After editing (current)", packages)

      this.changeUIstate(
        "editing",
        packages,
        this.state.loaded_packages,
        this.state.installed_packages,
        this.state.deleted_packages,
        this.state.requirements,
        this.state.kernel_name,
        this.state.thoth_config
      )

    }

    /**
     * Function: Edit saved row
     */

    editSavedRow(package_name: string, package_version: string) {

      const loaded_packages = this.state.loaded_packages
      const packages = this.state.packages

      _.unset(loaded_packages, package_name)
      _.set(packages, package_name, package_version)

      console.debug("After editing (initial)", loaded_packages)
      console.debug("After editing (current)", packages)

      this.changeUIstate(
        "editing",
        packages,
        loaded_packages,
        this.state.installed_packages,
        this.state.deleted_packages,
        this.state.requirements,
        this.state.kernel_name,
        this.state.thoth_config
      )

    }

    /**
     * Function: Delete row not saved
     */

    deleteRow(package_name: string) {

      const packages = this.state.packages

      const deleted_packages = {}

      _.unset(packages, package_name)

      console.debug("After deleting", packages)

      // TODO: Set correctly the version deleted
      _.set(deleted_packages, package_name, "*")

      console.debug("Deleted", deleted_packages)

      this.changeUIstate(
        "editing",
        packages,
        this.state.loaded_packages,
        this.state.installed_packages,
        deleted_packages,
        this.state.requirements,
        this.state.kernel_name,
        this.state.thoth_config
      )

    }

    /**
     * Function: Delete row saved
     */

    deleteSavedRow(package_name: string) {

      const saved_packages = this.state.loaded_packages

      _.unset(saved_packages, package_name)

      console.debug("After deleting saved", saved_packages)

      const deleted_packages = {}

      // TODO: Set correctly the version deleted
      _.set(deleted_packages, package_name, "*")

      console.debug("Deleted", deleted_packages)

      this.changeUIstate(
        "editing",
        this.state.packages,
        saved_packages,
        this.state.installed_packages,
        deleted_packages,
        this.state.requirements,
        this.state.kernel_name,
        this.state.thoth_config
      )
    }

    /**
     * Function: Store row when user requests it
     */

    storeRow(package_name: string, package_version: string) {

      let packages = this.state.packages

      _.set(packages, package_name, package_version)
      const new_dict: { [ name: string ]: string } = {}

      _.forIn(packages, function(value, key) {
        console.debug(key + ' goes ' + value);

        if ( key != "" ) {
          _.set(new_dict, key, value)
        }
      })

      console.debug("new packages", new_dict)

      this.changeUIstate(
        "editing",
        new_dict,
        this.state.loaded_packages,
        this.state.installed_packages,
        this.state.deleted_packages,
        this.state.requirements,
        this.state.kernel_name,
        this.state.thoth_config
      )

    }

    /**
     * Function: Save button to store every input in notebook
     */

    async onSave() {

      var packages_parsed = await _parse_packages_from_state(
        this.state.loaded_packages,
        this.state.packages
      )

      var deleted_case = await _handle_deleted_packages_case(
        this.state.deleted_packages,
        _.get(packages_parsed, "total_packages"),
        this.props.panel,
        this.state,
        _.get(packages_parsed, "new_packages")
      )

      if ( _.get(deleted_case, "relock") == true ) {
        await this.lock_using_thoth()
        return
      }

      if ( _.get(deleted_case, "go_to_state") == true ) {
        await this.setNewState(_.get(deleted_case, "new_state"));
        return
      }

      var new_state = await _handle_total_packages_case(
        _.get(packages_parsed, "total_packages"),
        this.props.panel,
        this.state
      )

      await this.setNewState(new_state);

    }

    async install() {

      var ui_state = this.state

      try {
          // Create new virtual environment and install dependencies using selected dependency manager (micropipenv by default)
          const install_message = await install_packages(
            this.state.kernel_name,
            this.state.resolution_engine
          );
          console.debug("Install message", install_message);

          _.set(ui_state, "status", "setting_kernel" )
          _.set(ui_state, "packages", {} )
          await this.setNewState(ui_state);
          return

      } catch ( error ) {

        console.debug("Error installing requirements", error)
        _.set(ui_state, "status", "failed")
        _.set(ui_state, "error_msg", "Error install dependencies in the new virtual environment, please contact Thoth team.")
        await this.setNewState(ui_state);
        return
      }
    }

    async setKernel() {

      var ui_state = this.state

      try {
          // Add new virtualenv to jupyter kernel so that it can be assigned to notebook.
          const message = await create_new_kernel( this.state.kernel_name );
          console.debug("Kernel message", message);

          _.set(ui_state, "status", "ready" )
          _.set(ui_state, "packages", {} )
          _.set(ui_state, "installed_packages", ui_state.loaded_packages )
          await this.setNewState(ui_state);
          return

        } catch ( error ) {

          console.debug("Error creating jupyter kernel", error)

          _.set(ui_state, "status", "failed")
          _.set(ui_state, "error_msg", "Error setting new environment in a jupyter kernel, please contact Thoth team.")
          await this.setNewState(ui_state);
          return

        }
    }

    async lock_using_thoth() {

      var ui_state = this.state

      _.set(ui_state, "status", "locking_requirements")
      await this.setNewState(ui_state);

      const notebook_content = await take_notebook_content( this.props.panel )

      try {

        var advise: Advise = await lock_requirements_with_thoth(
          this.state.kernel_name,
          notebook_content,
          JSON.stringify(this.state.thoth_config),
          JSON.stringify(this.state.requirements)
        );
        console.debug("Advise received", advise);

      } catch ( error ) {

        console.debug("Error locking requirements with Thoth", error)
        _.set(ui_state, "status", "locking_requirements_using_pipenv")
        await this.setNewState(ui_state);
        return
      }

      if ( advise.error == true ) {
        _.set(ui_state, "status", "locking_requirements_using_pipenv")
        await this.setNewState(ui_state);
        return
      }

      try {

        await set_notebook_metadata(
          this.props.panel,
          "thoth",
          advise.requirements,
          advise.requirement_lock,
          this.state.thoth_config
        )

      } catch ( error ) {
        console.debug("Error updating notebook metadata", error)
      }

      try {
        await store_dependencies_on_disk(
          this.state.kernel_name,
          advise.requirements,
          advise.requirement_lock,
          'overlays',
          false
        )
      } catch ( error ) {

        console.debug("Error storing dependencies in overlays", error)

      }

      try {
        await update_thoth_config_on_disk(
          this.state.thoth_config.runtime_environments[0],
          true
          )
        } catch ( error ) {
        console.debug("Error updating thoth config on disk", error)
      }

      _.set(ui_state, "status", "installing_requirements" )
      _.set(ui_state, "packages", {} )
      _.set(ui_state, "deleted_packages", {} )
      _.set(ui_state, "requirements", advise.requirements )
      _.set(ui_state, "resolution_engine", "thoth" )

      await this.setNewState(ui_state);
      return
  }


    async lock_using_pipenv () {

      var ui_state = this.state

      const notebookMetadataRequirements = this.state.requirements;
      console.debug("Requirements for pipenv", JSON.stringify(notebookMetadataRequirements));

      try {

        var result = await lock_requirements_with_pipenv(
          this.state.kernel_name,
          JSON.stringify(notebookMetadataRequirements)
        )
        console.debug("Result received", result);

      } catch ( error ) {

        console.debug("Error locking requirements with pipenv", error)

        _.set(ui_state, "status", "failed")
        _.set(ui_state, "error_msg", "Error asking advise to Thoth, , please contact Thoth team using: ")
        await this.setNewState(ui_state);
        return
      }

      if ( result.error == true ) {
        _.set(ui_state, "status", "failed")
        _.set(
          ui_state,
          "error_msg",
          "No resolution engine was able to install dependendices, please contact Thoth team using: "
        )
        await this.setNewState(ui_state);
        return
      }

      try {
        await set_notebook_metadata(
          this.props.panel,
          "pipenv",
          notebookMetadataRequirements,
          result.requirements_lock
        )

      } catch ( error ) {

        console.debug("Error storing metadata in notebook", error)

      }

      try {
        await store_dependencies_on_disk(
          this.state.kernel_name,
          notebookMetadataRequirements,
          result.requirements_lock,
          'overlays',
          false
        )

      } catch ( error ) {
        console.debug("Error storing dependencies in overlays", error)
      }

      try {
        await update_thoth_config_on_disk(
          this.state.thoth_config.runtime_environments[0],
          true
        )
      } catch ( error ) {
        console.debug("Error updating thoth config on disk", error)
      }

      _.set(ui_state, "status", "installing_requirements" )
      _.set(ui_state, "packages", {} )
      _.set(ui_state, "deleted_packages", {} )
      _.set(ui_state, "requirements", notebookMetadataRequirements )
      _.set(ui_state, "resolution_engine", "pipenv" )

      await this.setNewState(ui_state);
      return
    }

    async onStart() {

      // const script = `
      // print("This is jupyterlab-requirements")
      // `
      // await this.execute_code_in_kernel(script)

      var ui_on_start_state = await parse_inputs_from_metadata(
        this.state,
        this.props.panel,
        this.props.loaded_config_file,
        this.props.loaded_requirements,
        this.props.loaded_requirements_lock,
        this.props.loaded_resolution_engine
      )

      await this.setNewState(ui_on_start_state);
    }

    render(): React.ReactNode {

      let dependencyManagementform = <div>
                                        <DependencyManagementForm
                                          loaded_packages={this.state.loaded_packages}
                                          installed_packages={this.state.installed_packages}
                                          packages={this.state.packages}
                                          editRow={this.editRow}
                                          storeRow={this.storeRow}
                                          deleteRow={this.deleteRow}
                                          editSavedRow={this.editSavedRow}
                                          deleteSavedRow={this.deleteSavedRow}
                                        />
                                      </div>

      let addPlusInstallContainers = <div>
                                        <div className={CONTAINER_BUTTON}>
                                          <div className={CONTAINER_BUTTON_CENTRE}>
                                          <DependencyManagementNewPackageButton addNewRow={this.addNewRow} />
                                          </div>
                                        </div>
                                        <div className={CONTAINER_BUTTON}>
                                          <div className={CONTAINER_BUTTON_CENTRE}>
                                            <DependencyManagementInstallButton
                                            changeUIstate={this.changeUIstate}
                                            install={this.lock_using_thoth} />
                                          </div>
                                        </div>
                                      </div>

      let addPlusSaveContainers = <div>
                                      <div className={CONTAINER_BUTTON}>
                                        <div className={CONTAINER_BUTTON_CENTRE}>
                                        <DependencyManagementNewPackageButton addNewRow={this.addNewRow} />
                                        </div>
                                      </div>
                                      <div className={CONTAINER_BUTTON}>
                                        <div className={CONTAINER_BUTTON_CENTRE}>
                                          <DependencyManagementSaveButton
                                            onSave={this.onSave}
                                            changeUIstate={this.changeUIstate} />
                                        </div>
                                      </div>
                                    </div>

      let optionsForm = <div>
                        <section>
                          <h2>OPTIONS</h2>
                        </section>

                        <form>
                          <label>
                            Kernel name:
                            <input
                              title="Kernel name"
                              type="text"
                              name="kernel_name"
                              value={this.state.kernel_name}
                              onChange={this.setKernelName}
                            />
                          </label>
                          <br />
                          <label>
                            Recommendation type:
                            <select onChange={() => this.changeRecommendationType}>
                              title="Recommendation Type"
                              name="recommendation_type"
                              value={this.state.recommendation_type}
                              <option value="latest">latest</option>
                              <option value="performance">performance</option>
                              <option value="security">security</option>
                              <option value="stable">stable</option>
                            </select>
                          </label>
                          </form>
                      </div>

      var ui_status = this.state.status

      switch(ui_status) {

        case "loading":

          this.onStart()

          return (
            <div>
              Loading...
            </div>
          )

        case "initial":
          return (
            <div>
              <div className={CONTAINER_BUTTON}>
                <div className={CONTAINER_BUTTON_CENTRE}>
                <DependencyManagementNewPackageButton addNewRow={this.addNewRow} />
                </div>
              </div>
              <div>
                <fieldset>
                  <p> No dependencies found! Click New to add package. </p>
                </fieldset>
              </div>

            </div>
          );

        case "no_reqs_to_save":
          return (
            <div>
                {dependencyManagementform}
                {addPlusSaveContainers}
              <div>
                <fieldset>
                  <p> Dependencies missing! Click New to add package. </p>
                </fieldset>
              </div>
            </div>
          );

        case "only_install":
          return (
            <div>
              {dependencyManagementform}
              {addPlusInstallContainers}

              <div>
                <fieldset>
                  <p>Dependencies found in notebook metadata but lock file is missing. </p>
                </fieldset>
              </div>

              {optionsForm}
            </div>
          );

        case "only_install_kernel":
          return (
            <div>
              {dependencyManagementform}
              {addPlusInstallContainers}
              <div>
                <fieldset>
                  <p>Pinned down software stack found in notebook metadata!<br></br>
                  The kernel selected does not match the dependencies found for the notebook. <br></br>
                  Please install them.</p>
                </fieldset>
              </div>
              {optionsForm}
            </div>
          );

        case "only_install_kernel_runenv":
          return (
            <div>
              {dependencyManagementform}
              {addPlusInstallContainers}
              <div>
                <fieldset>
                  <p>Pinned down software stack found in notebook metadata!<br></br>
                  The runtime environment found in the notebook does not match your environment. <br></br>
                  Please use install button.</p>
                </fieldset>
              </div>
              {optionsForm}
            </div>
          );

        case "only_install_from_imports":

          return (
            <div>
              {dependencyManagementform}
              {addPlusInstallContainers}
              <div>
                <fieldset>
                  <p>No dependencies found in notebook metadata!<br></br>
                  Thoth identified the packages that are required to run this notebook from your code. <br></br>
                  Please use install button to install dependencies identified.</p>
                </fieldset>
              </div>
              {optionsForm}
            </div>
          );

        case "editing":
          return (
            <div>
              {dependencyManagementform}
              {addPlusSaveContainers}
            </div>
          );


        case "saved":
          return (
            <div>
              {dependencyManagementform}
              {addPlusInstallContainers}

              OPTIONS
              <div> Kernel name
                <input title="Kernel name"
                  className={THOTH_KERNEL_NAME_INPUT}
                  type="text"
                  name="kernel_name"
                  value={this.state.kernel_name}
                  onChange={this.setKernelName}
                />
              </div>
            </div>
          );

        case"locking_requirements":
          return (
            <div>
              {dependencyManagementform}
              <fieldset>
                <p>Contacting thoth for advise... please be patient!</p>
              </fieldset>
            </div>
          );

        case "installing_requirements":

          this.install()

          return (
            <div>
              {dependencyManagementform}
              <fieldset>
                <p>Requirements locked and saved!<br></br>
                Installing new requirements...
                </p>
              </fieldset>
            </div>
          );

      case "setting_kernel":

          this.setKernel()

          return (
            <div>
              {dependencyManagementform}
              <fieldset>
                <p>Requirements locked and saved!<br></br>
                Requirements installed!<br></br>
                Setting new kernel for your notebook...
                </p>
              </fieldset>
            </div>
          );


        case "failed_no_reqs":

          return (
            <div>
              <div>
                <button
                  title='Add requirements.'
                  className={OK_BUTTON_CLASS}
                  onClick={() => this.changeUIstate(
                    "loading",
                    this.state.packages,
                    this.state.loaded_packages,
                    this.state.installed_packages,
                    this.state.deleted_packages,
                    this.state.requirements,
                    this.state.kernel_name,
                    this.state.thoth_config,
                  )
                  }
                  >
                  Ok
                </button>
              </div>
              <div>
                <fieldset>
                  <p>No requirements have been added please click add after inserting package name!</p>
                </fieldset>
              </div>
            </div>
        );

        case "locking_requirements_using_pipenv":

          this.lock_using_pipenv()
          return (
            <div>
              <fieldset>
                <p>Thoth resolution engine failed... pipenv will be used to lock dependencies!</p>
              </fieldset>
            </div>
        );

        case "failed":

          return (
            <div>
              {dependencyManagementform}
              <div>
                <div className={CONTAINER_BUTTON}>
                  <div className={CONTAINER_BUTTON_CENTRE}>
                    <button
                      title='Finish.'
                      className={OK_BUTTON_CLASS}
                      onClick={() => this.changeUIstate(
                        "loading",
                        this.state.packages,
                        this.state.loaded_packages,
                        this.state.installed_packages,
                        this.state.deleted_packages,
                        this.state.requirements,
                        this.state.kernel_name,
                        this.state.thoth_config,
                      )
                      }
                      >
                      Ok
                    </button>
                  </div>
                </div>
              </div>
              <div>
                <p>{this.state.error_msg}</p>
              </div>
              <a href={"https://github.com/thoth-station/core/issues/new?assignees=&labels=&template=bug_report.md"} target="_blank"> Issue link </a>
            </div>
        );

        case "stable":

          return (
            <div>
              {dependencyManagementform}
              <div className={CONTAINER_BUTTON}>
                <div className={CONTAINER_BUTTON_CENTRE}>
                <DependencyManagementNewPackageButton addNewRow={this.addNewRow} />
                </div>
              </div>
              <div>
                <fieldset>
                  <p> Everything installed and ready to use!</p>
                </fieldset>
              </div>
            </div>
          );

          case "stable_no_runenv":
            // TODO: Provide relock button option if the resolution engine is different from thoth
            return (
              <div>
              {dependencyManagementform}
              <div className={CONTAINER_BUTTON}>
                <div className={CONTAINER_BUTTON_CENTRE}>
                <DependencyManagementNewPackageButton addNewRow={this.addNewRow} />
                </div>
              </div>
              <div>
                <fieldset>
                <p>Everything installed and ready to use!<br></br>
                    Keep in mind no runtime environment is present in the notebook metadata. <br></br>
                    Therefore your software stack might not be optimized for your environment. <br></br>
                    </p>
                </fieldset>
              </div>
            </div>
            );

        case"ready":

          this.props.panel.sessionContext.session.changeKernel({"name": this.state.kernel_name})

          return (
            <div>
              {dependencyManagementform}
              <div>
                <div className={CONTAINER_BUTTON}>
                    <div className={CONTAINER_BUTTON_CENTRE}>
                      <button
                        title='Reload Page and assign kernel.'
                        className={OK_BUTTON_CLASS}
                        onClick={() => this.changeUIstate(
                          "stable",
                          this.state.packages,
                          this.state.loaded_packages,
                          this.state.installed_packages,
                          this.state.deleted_packages,
                          this.state.requirements,
                          this.state.kernel_name,
                          this.state.thoth_config,
                        )
                        }
                        >
                        Ok
                      </button>
                    </div>
                </div>
              </div>
              <div>
                  <fieldset>
                    <p>Requirements locked and saved!<br></br>
                    Requirements installed!<br></br>
                    New kernel created!<br></br>
                    Click ok to start working on your notebook.<br></br>
                    </p>
                  </fieldset>
              </div>
            </div>
        );

    }
  }

  private _model: KernelModel;
}
