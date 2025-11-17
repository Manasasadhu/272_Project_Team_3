package com.research.agent.controller;

import com.research.agent.model.*;
import com.research.agent.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*", maxAge = 3600)
public class AuthController {

    private final AuthService authService;
    private static final String ERR_EMAIL_PASSWORD_REQUIRED = "Email and password are required";
    private static final String BEARER_PREFIX = "Bearer ";

    @Autowired
    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest loginRequest) {
        if (loginRequest == null || loginRequest.getEmail() == null || loginRequest.getPassword() == null) {
            return ResponseEntity.badRequest().body(
                new AuthResponse(false, ERR_EMAIL_PASSWORD_REQUIRED)
            );
        }

        AuthResponse response = authService.login(loginRequest.getEmail(), loginRequest.getPassword());
        return response.isSuccess() 
            ? ResponseEntity.ok(response) 
            : ResponseEntity.status(404).body(response);
    }

    @PostMapping("/signup")
    public ResponseEntity<AuthResponse> signup(@RequestBody SignupRequest signupRequest) {
        if (signupRequest == null || signupRequest.getEmail() == null || signupRequest.getPassword() == null) {
            return ResponseEntity.badRequest().body(
                new AuthResponse(false, ERR_EMAIL_PASSWORD_REQUIRED)
            );
        }

        AuthResponse response = authService.signup(signupRequest.getEmail(), signupRequest.getPassword());
        return response.isSuccess() 
            ? ResponseEntity.status(201).body(response) 
            : ResponseEntity.badRequest().body(response);
    }

    @GetMapping("/verify")
    public ResponseEntity<AuthResponse> verify(@RequestHeader(value = "Authorization", required = false) String token) {
        if (token == null || !token.startsWith(BEARER_PREFIX)) {
            return ResponseEntity.status(401).body(
                new AuthResponse(false, "Missing or invalid token")
            );
        }

        String actualToken = token.substring(BEARER_PREFIX.length()); // Remove prefix
        AuthResponse response = authService.verifyToken(actualToken);
        return response.isSuccess() 
            ? ResponseEntity.ok(response) 
            : ResponseEntity.status(401).body(response);
    }
}
