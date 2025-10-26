path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
path("select-company/", SelectCompanyView.as_view(), name="select_company"),
path("context/", ActiveContextView.as_view(), name="active_context"),
