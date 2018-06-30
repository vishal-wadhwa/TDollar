from Message.ActionButton import ActionButton
from Message.ActionMenu import ActionMenu
from Message.Message import Message
from Message.Attachment import Attachment
from Message.Confirm import Confirm
from Message.Field import Field
from Message.Option import Option
from Message.OptionGroup import OptionGroup


m = Message.Builder()
abtn = ActionButton.Builder()
amenu = ActionMenu.Builder()
att = Attachment.Builder()
cfm = Confirm.Builder()
fld = Field.Builder()
opt = Option.Builder()
optg = OptionGroup.Builder()

ob = (m.text('Test message')
        .attach(att.callback_id('ckckc')
                    .fallback('fbk_ctn')
                    .text('attach txt')
                    .title('att title')
                    .color(Attachment.COLOR_GOOD)
                    .addAction(amenu.name('menu')
                                    .text('menu details')
                                    .value('value_menu')
                                    .addOptionGroup(optg
                                        .text('g1')
                                        .addOption(opt.text('op1')
                                                        .value('op1v')
                                                        .descript('op1d')
                                                        .create())
                                        .addOption(opt.text('op2')
                                                        .value('op2v')
                                                        .descript('op2d')
                                                        .create())
                                        .create())
                                    .create())
                    .create())
        .attach(att.callback_id('ss')
                        .fallback('ffbk')
                        .text('some')
                        .title('ttl')
                        .title_link('https://google.com')
                        .addField(fld.title('t1')
                                        .value('val')
                                        .create())
                        .addField(fld.title('t2')
                                        .value('v2')
                                        .create())
                        .addAction(abtn
                                    .name('menu')
                                    .text('menu details')
                                    .value('value_menu')
                                    .confirm(cfm
                                                .text('Do you want to confirm?')
                                                .create())
                                    .create())
                        .create())
        .create())

print ob.to_json()