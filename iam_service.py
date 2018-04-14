class Iam:

    def __init__(self, iam_service):
        self.iam_service = iam_service

    def current_user(self, iam):
        current_user = self.iam_service.CurrentUser()

        return current_user