package com.research.agent.service;

import com.research.agent.model.AuthResponse;
import com.research.agent.model.AuthResponse.AuthData;
import com.research.agent.model.User;
import com.research.agent.repository.RedisUserRepository;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

@Service
public class AuthServiceImpl implements AuthService {

    private final RedisUserRepository userRepository;
    private final RedisTemplate<String, String> redisTemplate;
    private static final String TOKEN_PREFIX = "token:";
    private static final long TOKEN_EXPIRATION = 24; // 24 hours
    private static final TimeUnit TOKEN_EXPIRATION_UNIT = TimeUnit.HOURS;

    public AuthServiceImpl(RedisUserRepository userRepository, RedisTemplate<String, String> redisTemplate) {
        this.userRepository = userRepository;
        this.redisTemplate = redisTemplate;
    }

    @Override
    public AuthResponse login(String email, String password) {
        // Validate input
        if (email == null || email.trim().isEmpty() || password == null || password.trim().isEmpty()) {
            return new AuthResponse(false, "Email and password cannot be empty");
        }

        // Validate user credentials against Redis
        Long userId = userRepository.validateUser(email, password);
        if (userId == null) {
            return new AuthResponse(false, "Invalid email or password");
        }

        // Generate token
        String token = UUID.randomUUID().toString();
        String tokenKey = TOKEN_PREFIX + token;
        redisTemplate.opsForValue().set(tokenKey, String.valueOf(userId), TOKEN_EXPIRATION, TOKEN_EXPIRATION_UNIT);

        // Create response
        User user = new User(userId, email);
        AuthData authData = new AuthData(user, token);
        return new AuthResponse(true, "Login successful", authData);
    }

    @Override
    public AuthResponse signup(String email, String password) {
        // Validate input
        if (email == null || email.trim().isEmpty() || password == null || password.trim().isEmpty()) {
            return new AuthResponse(false, "Email and password cannot be empty");
        }

        // Check if user already exists
        if (userRepository.emailExists(email)) {
            return new AuthResponse(false, "User already exists with this email");
        }

        // Create new user in Redis
        Long userId = userRepository.saveUser(email, password);
        if (userId == null) {
            return new AuthResponse(false, "Failed to create user");
        }

        // Generate token
        String token = UUID.randomUUID().toString();
        String tokenKey = TOKEN_PREFIX + token;
        redisTemplate.opsForValue().set(tokenKey, String.valueOf(userId), TOKEN_EXPIRATION, TOKEN_EXPIRATION_UNIT);

        // Create response
        User user = new User(userId, email);
        AuthData authData = new AuthData(user, token);
        return new AuthResponse(true, "Signup successful", authData);
    }

    @Override
    public AuthResponse verifyToken(String token) {
        // Validate token
        if (token == null || token.trim().isEmpty()) {
            return new AuthResponse(false, "Token cannot be empty");
        }

        // Check if token exists in Redis
        String tokenKey = TOKEN_PREFIX + token;
        String userIdStr = redisTemplate.opsForValue().get(tokenKey);
        if (userIdStr == null) {
            return new AuthResponse(false, "Invalid or expired token");
        }

        // Get user details
        Long userId = Long.parseLong(userIdStr);
        User user = userRepository.getUserById(userId);
        if (user == null) {
            return new AuthResponse(false, "User not found");
        }

        AuthData authData = new AuthData(user, token);
        return new AuthResponse(true, "Token verified", authData);
    }
}
