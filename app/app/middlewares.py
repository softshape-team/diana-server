from django.contrib.auth import get_user_model


User = get_user_model()


class UpdateAPILoginResponse:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.path_info != "/accounts/login/"
            or request.method != "POST"
            or response.status_code != 200
        ):
            return response

        user = User.objects.get(pk=response.data["user"]["pk"])

        response.data["user"]["birthdate"] = user.birthdate
        try:
            response.data["user"]["image"] = user.image.url
        except ValueError:
            pass

        response._is_rendered = False
        response.render()

        return response
