API_STRUCTURE = {
    "Login" :{
        "POST":"main_account.login_handler"
    },
    "Register":{
        "POST":"main_account.register_handler"
    },
    "Logout":{
        "POST":"main_account.logout_handler"
    },
    "SubAccount":{
        "GET":"sub_account.api_get_sub_accounts",
        "DELETE":"sub_account.api_delete_sub_accounts",
        "POST":"sub_account.api_post_sub_accounts",
        "PUT":"sub_account.api_put_sub_accounts",
        "Login":{
            "POST":"sub_account.api_login_sub_account"
        },
        "Logout":{
            "POST":"sub_account.api_logout_sub_account"
        }
    }
}