"""
A program to register Kivy Cupertino widgets for use in kv lang
"""

from kivy.factory import Factory

Factory.register('CupertinoNavigationBar', module='kivycupertino.uix.bar')
Factory.register('CupertinoButton', module='kivycupertino.uix.button')
Factory.register('CupertinoSystemButton', module='kivycupertino.uix.button')
Factory.register('CupertinoIconButton', module='kivycupertino.uix.button')
Factory.register('CupertinoDialogButton', module='kivycupertino.uix.button')
Factory.register('CupertinoAlertDialog', module='kivycupertino.uix.dialog')
Factory.register('CupertinoProgressBar', module='kivycupertino.uix.indicator')
Factory.register('CupertinoLabel', module='kivycupertino.uix.label')
Factory.register('CupertinoSwitch', module='kivycupertino.uix.switch')
Factory.register('CupertinoTextField', module='kivycupertino.uix.textfield')
Factory.register('CupertinoTextView', module='kivycupertino.uix.textfield')
