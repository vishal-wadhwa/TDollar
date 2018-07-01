from Message.ActionMenu import ActionMenu
from Message.Attachment import Attachment
from Message.Option import Option
from Message.OptionGroup import OptionGroup
import json

ab = Attachment.Builder()
ogb = OptionGroup.Builder()
ob = Option.Builder()
menub = ActionMenu.Builder()

msg_at = json.dumps([ab.callback_id('dd_bidtype_select')
                            .fallback('No support for selection')
                            .text('Choose wisely')
                            .title('Options:')
                            .color(Attachment.COLOR_GOOD)
                            .addAction(menub.name('Bid menu')
                                            .text('Bid Menu')
                                            .addOptionGroup(ogb.text('Games')
                                                                .addOption(ob.text('Table Tennis')
                                                                                .value('table_tennis')
                                                                                .create())
                                                                .addOption(ob.text('Foosball')
                                                                                .value('foosball')
                                                                                .create())
                                                                .create())
                                            .addOptionGroup(ogb.text('Leisure')
                                                                .addOption(ob.text('Massage Chair')
                                                                                .value('massage_chair')
                                                                                .create())
                                                                .addOption(ob.text('Leg massager')
                                                                                .value('leg_massager')
                                                                                .create())
                                                                .create())
                                            .create())
                            .create().to_dict()])

