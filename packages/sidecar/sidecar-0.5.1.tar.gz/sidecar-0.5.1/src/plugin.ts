// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  JupyterLab, JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
    UUID
} from '@lumino/coreutils';

import {
  IJupyterWidgetRegistry, WidgetView
} from '@jupyter-widgets/base';

import {
  output
} from '@jupyter-widgets/jupyterlab-manager';

import {
  SidecarModel
} from './widget';

import {
  EXTENSION_SPEC_VERSION
} from './version';

import '../css/sidecar.css';

const EXTENSION_ID = '@jupyter-widgets/jupyterlab-sidecar';

const sidecarPlugin: JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default sidecarPlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: JupyterLab, registry: IJupyterWidgetRegistry): void {
    let SidecarView = class extends output.OutputView {
      model: SidecarModel;

      render() {
        if (!this.model.rendered) {
          super.render();

          let w = this._outputView;
          w.addClass('jupyterlab-sidecar');
          w.addClass('jp-LinkedOutputView');
          w.title.label = this.model.get('title');
          w.title.closable = true;
          app.shell['_rightHandler'].sideBar.tabCloseRequested.connect((sender : any, tab : any) => {
              tab.title.owner.dispose();
          });
          w.id = UUID.uuid4();

          if (Object.keys(this.model.views).length > 1) {
            w.node.style.display = 'none';
            let key = Object.keys(this.model.views)[0];
            this.model.views[key].then((v: WidgetView) => {
              if (v instanceof output.OutputView) {
                v._outputView.activate();
              }
            });
          } else {
            let anchor = this.model.get('anchor') || 'right';
            if(anchor === 'right'){
              app.shell.add(w, 'right');
            } else {
              app.shell.add(w, 'main', {mode: anchor});
            }
            app.shell.activateById(w.id);
          }
        }
      }
    }

    registry.registerWidget({
      name: '@jupyter-widgets/jupyterlab-sidecar',
      version: EXTENSION_SPEC_VERSION,
      exports: {
        // @ts-ignore: Why is this not compiling?
        SidecarModel, SidecarView
      }
  });
}
