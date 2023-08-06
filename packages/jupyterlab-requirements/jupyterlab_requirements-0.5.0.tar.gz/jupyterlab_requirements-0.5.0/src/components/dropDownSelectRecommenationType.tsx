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

import React from 'react';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

/**
 * Class: Holds properties for DependencyManagementInstallButton.
 */

export interface IProps {
    method: Function,
    recommendation_type: string
  }

export interface IState {
    recommendation: string;
}


export class DropDownSelectRecommendationType extends React.Component<IProps, IState> {
    constructor(props: IProps) {
      super(props);
      this.state = {
        recommendation: this.props.recommendation_type
        };
    }

    render() {
        return (
            <FormControl>
                <InputLabel>Recommendation</InputLabel>
                <Select
                    value={this.state.recommendation}
                    onSelect={() => this.props.method()}
                    label="Recommendation"
                    >
                    <MenuItem value="latest">
                        <em>latest</em>
                    </MenuItem>
                        <MenuItem value={"latest"}>latest</MenuItem>
                        <MenuItem value={"performance"}>performance</MenuItem>
                        <MenuItem value={"security"}>security</MenuItem>
                        <MenuItem value={"stable"}>stable</MenuItem>
                </Select>
            </FormControl>
        );
        }
    }
