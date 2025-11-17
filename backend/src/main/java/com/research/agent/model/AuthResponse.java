package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AuthResponse {
    @JsonProperty("success")
    private boolean success;

    @JsonProperty("message")
    private String message;

    @JsonProperty("data")
    private AuthData data;

    @JsonProperty("error")
    private String error;

    public AuthResponse() {}

    public AuthResponse(boolean success, String message) {
        this.success = success;
        this.message = message;
    }

    public AuthResponse(boolean success, String message, AuthData data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }

    public static class AuthData {
        @JsonProperty("user")
        private User user;

        @JsonProperty("token")
        private String token;

        public AuthData() {}

        public AuthData(User user, String token) {
            this.user = user;
            this.token = token;
        }

        public User getUser() {
            return user;
        }

        public void setUser(User user) {
            this.user = user;
        }

        public String getToken() {
            return token;
        }

        public void setToken(String token) {
            this.token = token;
        }
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public AuthData getData() {
        return data;
    }

    public void setData(AuthData data) {
        this.data = data;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }
}
