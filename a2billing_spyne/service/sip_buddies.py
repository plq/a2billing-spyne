# encoding: utf8
#
# This file is part of the a2billing-spyne project.
# Copyright (c), Arskom Ltd. (arskom.com.tr),
#                Cemrecan Ünal <unalcmre@gmail.com>.
#                Burak Arslan <burak.arslan@arskom.com.tr>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the Arskom Ltd. nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from contextlib import closing

from twisted.internet.threads import deferToThread

from spyne import rpc

from neurons.form import HtmlForm

from a2billing_spyne.model import SipBuddies
from a2billing_spyne.service import ReaderServiceBase, ScreenBase, DalBase


class NewSipScreen(ScreenBase):
    main = SipBuddies.customize(
        prot=HtmlForm(), form_action="put_sip",
        child_attrs_all=dict(
            exc=True,
        ),
        child_attrs=dict(
            id=dict(order=0, write=False, exc=False),
        ),
    )


class SipDal(DalBase):
    def put_sip(self, sip):
        with closing(self.ctx.app.config.get_main_store().Session()) as session:
            session.add(sip)
            session.commit()


class SipReaderServices(ReaderServiceBase):
    @rpc(SipBuddies, _returns=NewSipScreen, _body_style='bare')
    def new_sip_buddy(ctx, sip):
        return NewSipScreen(title="Echo Sip", main=sip)


class SipWriterServices(ReaderServiceBase):
    @rpc(SipBuddies, _body_style='bare')
    def put_sip(ctx, sip):
        return deferToThread(SipDal(ctx).put_sip, sip)
