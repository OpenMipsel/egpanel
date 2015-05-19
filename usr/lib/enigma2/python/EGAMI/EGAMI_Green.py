from enigma import getDesktop
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.config import *
from Components.UsageConfig import *
from Components.ConfigList import *
from Components.PluginList import *
from Components.Sources.List import List
from Components.PluginComponent import plugins
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
import os
from EGAMI.EGAMI_tools import *
from Plugins.Extensions.EGAMIPermanentClock.plugin import *

class EGDecodingSetup(ConfigListScreen, Screen):

    def __init__(self, session, args = 0):
        Screen.__init__(self, session)
        self.skinName = ['Setup']
        Screen.setTitle(self, _('Decoding Setup'))
        list = []
        list.append(getConfigListEntry(_('Show No free tuner info'), config.usage.messageNoResources))
        list.append(getConfigListEntry(_('Show Tune failed info'), config.usage.messageTuneFailed))
        list.append(getConfigListEntry(_('Show No data on transponder info'), config.usage.messageNoPAT))
        list.append(getConfigListEntry(_('Show Service not found info'), config.usage.messageNoPATEntry))
        list.append(getConfigListEntry(_('Show Service invalid info'), config.usage.messageNoPMT))
        list.append(getConfigListEntry(_('Hide CI Messages'), config.usage.hide_ci_messages))
        list.append(getConfigListEntry(_('Hide zap errors'), config.usage.hide_zap_errors))
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        ConfigListScreen.__init__(self, list)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'red': self.dontSaveAndExit,
         'green': self.saveAndExit,
         'cancel': self.dontSaveAndExit}, -1)

    def saveAndExit(self):
        if config.usage.dsemudmessages.value is not False:
            os.system('rm -rf /var/etc/.no_osd_messages')
        elif config.usage.dsemudmessages.value is not True:
            os.system('touch /var/etc/.no_osd_messages')
        if config.usage.messageYesPmt.value is not False:
            os.system('rm -rf /var/etc/.no_pmt_tmp')
        elif config.usage.messageYesPmt.value is not True:
            os.system('touch /var/etc/.no_pmt_tmp')
        for x in self['config'].list:
            x[1].save()

        config.usage.save()
        self.close()

    def dontSaveAndExit(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()


config.infobar = ConfigSubsection()
config.infobar.weatherEnabled = ConfigYesNo(default=False)
config.infobar.permanentClockPosition = ConfigSelection(choices=['<>'], default='<>')
config.infobar.Ecn = ConfigYesNo(default=True)
config.infobar.CamName = ConfigYesNo(default=True)
config.infobar.NetInfo = ConfigYesNo(default=True)
config.infobar.EcmInfo = ConfigYesNo(default=True)
config.infobar.CryptoBar = ConfigYesNo(default=True)

class EGInfoBarSetup(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = ['Setup']
        Screen.setTitle(self, _('Infobar Setup'))
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['description'] = Label(_('* = Restart Required'))
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.keySave,
         'back': self.keyCancel,
         'red': self.keyCancel}, -2)
        self.list.append(getConfigListEntry(_('1st infobar timeout'), config.usage.infobar_timeout))
        self.list.append(getConfigListEntry(_('Show 2nd infobar'), config.usage.show_second_infobar))
        self.list.append(getConfigListEntry(_('2nd infobar timeout'), config.usage.second_infobar_timeout))
        self.list.append(getConfigListEntry(_('2nd infobar style*'), config.usage.second_infobar_style))
        self.list.append(getConfigListEntry(_('Show infobar picons'), config.usage.showpicon))
        self.list.append(getConfigListEntry(_('Enable infobar fade-out'), config.usage.show_infobar_do_dimming))
        self.list.append(getConfigListEntry(_('Infobar fade-out speed'), config.usage.show_infobar_dimming_speed))
        self.list.append(getConfigListEntry(_('Show Weather on channel change'), config.infobar.weatherEnabled))
        self.list.append(getConfigListEntry(_('Show PVR status in Movie Player'), config.usage.show_event_progress_in_servicelist))
        self.list.append(getConfigListEntry(_('Show channel number in infobar'), config.usage.show_infobar_channel_number))
        self.list.append(getConfigListEntry(_('Show infobar on channel change'), config.usage.show_infobar_on_zap))
        self.list.append(getConfigListEntry(_('Show infobar on skip forward/backward'), config.usage.show_infobar_on_skip))
        self.list.append(getConfigListEntry(_('Show infobar on event change'), config.usage.movieplayer_pvrstate))
        self.list.append(getConfigListEntry(_('Infobar frontend data source'), config.usage.infobar_frontend_source))
        self.list.append(getConfigListEntry(_('Show Source Info'), config.infobar.Ecn))
        self.list.append(getConfigListEntry(_('Show SoftCam name'), config.infobar.CamName))
        self.list.append(getConfigListEntry(_('Show Netcard Info'), config.infobar.NetInfo))
        self.list.append(getConfigListEntry(_('Show ECM-Info'), config.infobar.EcmInfo))
        self.list.append(getConfigListEntry(_('Show Crypto-Bar'), config.infobar.CryptoBar))
        self.list.append(getConfigListEntry(_('Show EIT now/next in infobar'), config.usage.show_eit_nownext))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)

    def keyRight(self):
        ConfigListScreen.keyRight(self)

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        self.close()

    def keyCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()


class EGClockSetup(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = ['Setup']
        Screen.setTitle(self, _('Permanental Clock Setup'))
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['description'] = Label(_('* = Restart Required'))
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.keySave,
         'back': self.keyCancel,
         'red': self.keyCancel}, -2)
        self.list.append(getConfigListEntry(_('Show permanental clock'), config.plugins.PermanentClock.enabled))
        self.list.append(getConfigListEntry(_('\tSet clock position'), config.infobar.permanentClockPosition))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.handleKeysLeftAndRight()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.handleKeysLeftAndRight()

    def handleKeysLeftAndRight(self):
        sel = self['config'].getCurrent()[1]
        if sel == config.infobar.permanentClockPosition:
            pClock.dialog.hide()
            self.session.openWithCallback(self.positionerCallback, PermanentClockPositioner)

    def positionerCallback(self, callback = None):
        pClock.showHide()

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        if pClock.dialog is None:
            pClock.gotSession(self.session)
        if config.plugins.PermanentClock.enabled.value == True:
            pClock.showHide()
        if config.plugins.PermanentClock.enabled.value == False:
            pClock.showHide()
        self.close()
        return

    def keyCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()


class EGUpdateSetup(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = ['Setup']
        Screen.setTitle(self, _('Update Setup'))
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['description'] = Label(_('* = Restart Required'))
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Save'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.keySave,
         'back': self.keyCancel,
         'save': self.keyCancel}, -2)
        self.list.append(getConfigListEntry(_('Prioritize updates of packages (--force-overwrite)'), config.usage.use_force_overwrite))
        self.list.append(getConfigListEntry(_('Use package maintainer config files'), config.usage.use_package_conffile))
        self.list.append(getConfigListEntry(_('Show popup message when update available'), config.usage.show_notification_for_updates))
        self.list.append(getConfigListEntry(_('Check update every (hours)'), config.usage.check_for_updates))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)

    def keyRight(self):
        ConfigListScreen.keyRight(self)

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        self.close()

    def keyCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()


class EGGreenPanel(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen name="EGGreenPanel" position="center,100" size="1080,920" title="EGAMI Green Panel" >\n\t\t\t\t<widget source="list" render="Listbox" position="10,0" size="1070,830" zPosition="2" scrollbarMode="showOnDemand" transparent="1">\n\t\t\t\t      <convert type="TemplatedMultiContent">\n\t\t\t\t\t  {"template": [\n\t\t\t\t\t  MultiContentEntryText(pos = (175, 0), size = (950, 35), font=0, text = 0),\n\t\t\t\t\t  MultiContentEntryText(pos = (175, 38), size = (950, 28), font=1, text = 1),\n\t\t\t\t\t  MultiContentEntryPixmapAlphaTest(pos = (6, 5), size = (150, 60), png = 2),\n\t\t\t\t\t  ],\n\t\t\t\t\t  "fonts": [gFont("Regular", 32),gFont("Regular", 26)],\n\t\t\t\t\t  "itemHeight": 80\n\t\t\t\t\t  }\n\t\t\t\t      </convert>\n\t\t\t\t</widget>\n\t\t\t\t<ePixmap position="40,854" size="100,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="220,854" size="100,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="430,854" size="100,40" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="740,854" size="100,40" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<widget name="key_red" position="80,854" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="red" transparent="1" />\n\t\t\t\t<widget name="key_green" position="260,854" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="green" transparent="1" />\n\t\t\t\t<widget name="key_yellow" position="470,854" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="yellow" transparent="1" />\n\t\t\t\t<widget name="key_blue" position="780,854" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="blue" transparent="1" />\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen name="EGGreenPanel" position="center,center" size="700,560" title="EGAMI Green Panel" >\n\t\t\t\t<widget name="Addons" zPosition="4" position="50,520" size="140,40" halign="left" font="Regular;22" transparent="1" />\n\t\t\t\t<widget name="Extras" zPosition="4" position="230,520" size="140,40" halign="left" font="Regular;22" transparent="1" />\n\t\t\t\t<widget name="File Mode" zPosition="4" position="400,520" size="140,40" halign="left" font="Regular;22" transparent="1" />\n\t\t\t\t<widget name="Scripts" zPosition="4" position="580,520" size="140,40" halign="left" font="Regular;22" transparent="1"  />\n\t\t\t\t<ePixmap name="key_red_png" pixmap="skin_default/buttons/button_red.png" position="20,520" size="140,40" alphatest="on" />\n\t\t\t\t<ePixmap name="key_green_png" pixmap="skin_default/buttons/button_green.png" position="200,520" size="140,40" alphatest="on" />\n\t\t\t\t<ePixmap name="key_yellow_png" pixmap="skin_default/buttons/button_yellow.png" position="370,520" size="140,40" alphatest="on" />\n\t\t\t\t<ePixmap name="key_blue_png" pixmap="skin_default/buttons/button_blue.png" position="550,520" size="140,40" alphatest="on" />\n\t\t\t\t<widget source="list" render="Listbox" position="10,0" size="680,510" zPosition="2" scrollbarMode="showOnDemand" transparent="1">\n\t\t\t\t      <convert type="TemplatedMultiContent">\n\t\t\t\t\t  {"template": [\n\t\t\t\t\t  MultiContentEntryText(pos = (125, 0), size = (650, 24), font=0, text = 0),\n\t\t\t\t\t  MultiContentEntryText(pos = (125, 24), size = (650, 24), font=1, text = 1),\n\t\t\t\t\t  MultiContentEntryPixmapAlphaTest(pos = (6, 5), size = (100, 40), png = 2),\n\t\t\t\t\t  ],\n\t\t\t\t\t  "fonts": [gFont("Regular", 24),gFont("Regular", 20)],\n\t\t\t\t\t  "itemHeight": 50\n\t\t\t\t\t  }\n\t\t\t\t      </convert>\n\t\t\t\t</widget>\n\t\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('EGAMI Green Panel'))
        self.list = []
        self['list'] = List(self.list)
        self['key_red'] = Label(_('Addons'))
        self['key_green'] = Label(_('Panel'))
        self['key_yellow'] = Label(_('File Commander'))
        self['key_blue'] = Label(_('Scripts'))
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.save,
         'back': self.close,
         'red': self.Addons,
         'yellow': self.File,
         'green': self.Extras,
         'blue': self.Script}, -1)
        self.onFirstExecBegin.append(self.checkWarnings)

    def save(self):
        self.run()

    def run(self):
        mysel = self['list'].getCurrent()
        if mysel:
            plugin = mysel[3]
            plugin(session=self.session)

    def updateList(self):
        self.list = []
        self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
        for plugin in self.pluginlist:
            if plugin.icon is None:
                png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/icons/plugin.png'))
            else:
                png = plugin.icon
            res = (plugin.name,
             plugin.description,
             png,
             plugin)
            self.list.append(res)

        self['list'].list = self.list
        return

    def reloadPluginList(self):
        plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
        self.updateList()

    def checkWarnings(self):
        if len(plugins.warnings):
            text = _('Some plugins are not available:\n')
            for pluginname, error in plugins.warnings:
                text += _('%s (%s)\n') % (pluginname, error)

            plugins.resetWarnings()
            self.session.open(MessageBox, text=text, type=MessageBox.TYPE_WARNING)

    def Addons(self):
        m = checkkernel()
        if m == 1:
            from EGAMI.EGAMI_addon_manager import EGAddonMenu
            self.session.openWithCallback(self.reloadPluginList, EGAddonMenu)
        else:
            self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)

    def File(self):
        m = checkkernel()
        if m == 1:
            from Plugins.Extensions.FileCommander.plugin import FileCommanderScreen
            self.session.open(FileCommanderScreen)
        else:
            self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)

    def Script(self):
        m = checkkernel()
        if m == 1:
            from EGAMI.EGAMI_main import EGScript
            self.session.open(EGScript)
        else:
            self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)

    def Extras(self):
        m = checkkernel()
        if m == 1:
            from EGAMI.EGAMI_main import EgamiMainPanel
            self.session.open(EgamiMainPanel)
        else:
            self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
