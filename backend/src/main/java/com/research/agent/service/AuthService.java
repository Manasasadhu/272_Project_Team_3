package com.research.agent.service;

import com.research.agent.model.AuthResponse;

public interface AuthService {
    AuthResponse login(String email, String password);

    AuthResponse signup(String email, String password);

    AuthResponse verifyToken(String token);
}
