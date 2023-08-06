from tonclient.decorators import result_as
from tonclient.module import TonModule
from tonclient.types import ParamsOfStart, RegisteredDebot, ParamsOfFetch, \
    ParamsOfExecute, ParamsOfSend, ResponseHandler


class TonDebot(TonModule):
    """ Free TON debot SDK API implementation """
    @result_as(classname=RegisteredDebot)
    def start(
            self, params: ParamsOfStart,
            callback: ResponseHandler) -> RegisteredDebot:
        """
        Starts an instance of debot.
        Downloads debot smart contract from blockchain and switches it to
        context zero. Returns a debot handle which can be used later in
        execute function. This function must be used by Debot Browser to
        start a dialog with debot. While the function is executing, several
        Browser Callbacks can be called, since the debot tries to display all
        actions from the context 0 to the user.

        `start` is equivalent to `fetch` + switch to context 0
        :param params: See `types.ParamsOfStart`
        :param callback: Callback for debot events
        :return: See `types.RegisteredDebot`
        """
        return self.request(
            method='debot.start', callback=callback, **params.dict)

    @result_as(classname=RegisteredDebot)
    def fetch(
            self, params: ParamsOfFetch,
            callback: ResponseHandler) -> RegisteredDebot:
        """
        Fetches debot from blockchain.
        Downloads debot smart contract (code and data) from blockchain and
        creates an instance of Debot Engine for it.

        It does not switch debot to context 0. Browser Callbacks are not
        called
        :param params: See `types.ParamsOfFetch`
        :param callback: Callback for debot events
        :return: See `types.RegisteredDebot`
        """
        return self.request(
            method='debot.fetch', callback=callback, **params.dict)

    def execute(self, params: ParamsOfExecute):
        """
        Executes debot action.
        Calls debot engine referenced by debot handle to execute input action.
        Calls Debot Browser Callbacks if needed.

        Chain of actions can be executed if input action generates a list of
        subactions
        :param params: See `types.ParamsOfExecute`
        :return:
        """
        return self.request(method='debot.execute', **params.dict)

    def send(self, params: ParamsOfSend):
        """
        Sends message to Debot.
        Used by Debot Browser to send response on DInterface call or from
        other Debots
        :param params: See `types.ParamsOfSend`
        :return:
        """
        return self.request(method='debot.send', **params.dict)

    def remove(self, params: RegisteredDebot):
        """
        Destroys debot handle.
        Removes handle from Client Context and drops debot engine referenced
        by that handle
        :param params: See `types.RegisteredDebot`
        :return:
        """
        return self.request(method='debot.remove', **params.dict)
