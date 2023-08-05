import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { requestAPI } from './handler';
import { ITopBar } from 'jupyterlab-topbar';
import { Toolbar } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { Menu } from '@lumino/widgets';

/**
 * Initialization data for jupyterlab-gpulab server extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-gpulab',
  autoStart: true,
  requires: [ITopBar, ICommandPalette, IMainMenu],
  activate: async (
      app: JupyterFrontEnd,
      topBar: ITopBar,
      palette: ICommandPalette,
      mainMenu: IMainMenu,
  ) => {
    console.log('JupyterLab extension server-extension-example is activated!');
    document.title = 'GPULab | JupyterLab Environment'

    const header = new Toolbar()
    header.id = 'gpulab-header'
    header.addClass('jp-gpulab-header')

    const logoWidget = new Widget();
    logoWidget.id = 'gpulab-logo'
    logoWidget.addClass('jp-gpulab-logo')

    // const verButton = new ToolbarButton({
    //   className: 'jp-gpulab-msg-button',
    //   label: "",
    // })

    header.addItem("logo", logoWidget)
    header.addItem("spcaer", Toolbar.createSpacerItem())
    // header.addItem("version", verButton)

    app.shell.add(header, "header", undefined)

    const {commands} = app;
    const portal_command = 'gpulab:launch_portal';
    const blog_command = 'gpulab:launch_blog';
    const faq_command = 'gpulab:launch_faq';
    const contact_command = 'gpulab:launch_contact';
    const twitter_command = 'gpulab:twitter';
    const github_command = 'gpulab:github';

    commands.addCommand(portal_command, {
      label: 'GPULab Account Portal',
      caption: 'Open the GPULab portal.',
      execute: (args: any) => {
        window.open(`https://portal.gpulab.io`, 'gpulab-external');
      }
    });

    commands.addCommand(blog_command, {
      label: 'GPULab Blog',
      caption: 'Open the GPULab blog/',
      execute: (args: any) => {
        window.open(`https://gpulab.io/blog/`, 'gpulab-external');
      }
    });

    commands.addCommand(faq_command, {
      label: 'GPULab FAQ',
      caption: 'Open the GPULab FAQ page.',
      execute: (args: any) => {
        window.open(`https://gpulab.io/faq/`, 'gpulab-external');
      }
    });

    commands.addCommand(contact_command, {
      label: 'GPULab Contact',
      caption: 'Open the GPULab contact page.',
      execute: (args: any) => {
        window.open(`https://gpulab.io/blog/`, 'gpulab-external');
      }
    });

    commands.addCommand(twitter_command, {
      label: 'GPULab Twitter',
      caption: 'Follow GPULab on Twitter.',
      execute: (args: any) => {
        window.open(`https://twitter.com/gpulabio`, 'gpulab-external');
      }
    });

    commands.addCommand(github_command, {
      label: 'GPULab GitHub',
      caption: 'GPULab GitHub repository.',
      execute: (args: any) => {
        window.open(`https://github.com/gpulab`, 'gpulab-external');
      }
    });

    const category = 'GPULab';

    palette.addItem({command: portal_command, category: category, args: {}});
    palette.addItem({command: blog_command, category: category, args: {}});
    palette.addItem({command: faq_command, category: category, args: {}});
    palette.addItem({command: contact_command, category: category, args: {}});


    // Create a GPULab Menu
    const gpuLabMenu: Menu = new Menu({ commands });
    gpuLabMenu.title.label = 'GPULab';
    mainMenu.addMenu(gpuLabMenu, { rank: 1000 });

    gpuLabMenu.addItem({ command: portal_command, args: {}});
    gpuLabMenu.addItem({ command: blog_command, args: {}});
    gpuLabMenu.addItem({ command: faq_command, args: {}});
    gpuLabMenu.addItem({ command: contact_command, args: {}});
    gpuLabMenu.addItem({ command: twitter_command, args: {}});
    gpuLabMenu.addItem({ command: github_command, args: {}});

    const gpuUtlWidget = new Widget();
    const gpuMemWidget = new Widget();
    // const gpuPwrWidget = new Widget();
    const storageWidget = new Widget();

    update();
    topBar.addItem('storage', storageWidget);
    // topBar.addItem('gpu_pwr', gpuPwrWidget);
    topBar.addItem('gpu_mem', gpuMemWidget);
    topBar.addItem('gpu_utl', gpuUtlWidget);

    setInterval(update, 5000);

    function update() {
      requestAPI<any>('metrics')
          .then(data => {
            gpuUtlWidget.node.textContent =
                'GPU: ' + data['gpu']['utilization.gpu'] + '%';
            gpuMemWidget.node.textContent =
                'GPU Mem: ' +
                data['gpu']['memory.used'] +
                ' of ' +
                data['gpu']['memory.total'] +
                'MB';
            storageWidget.node.textContent =
                'Storage Used ' +
                data['storage']['used'] +
                ' / ' +
                data['storage']['free'] + ' Free';
            // gpuPwrWidget.node.textContent =
            //     'GPU Pwr: ' +
            //     data['gpu']['power.draw'] +
            //     ' / ' +
            //     data['gpu']['power.max_limit'] +
            //     'W';
          })
          .catch(reason => {
            console.error(
                `The jupyterlab_gpulab_service_info server extension appears to be missing.\n${reason}`
            );
          });
    }

  }
};

export default extension;
