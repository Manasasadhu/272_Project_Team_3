package com.research.agent.repository;

import com.research.agent.model.User;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Repository;
import java.util.concurrent.TimeUnit;

@Repository
public class RedisUserRepository {

    private final RedisTemplate<String, String> redisTemplate;
    private static final String USER_PREFIX = "user:";
    private static final String EMAIL_ID_PREFIX = "email_to_id:";
    private static final String USER_ID_COUNTER = "user_id_counter";
    private static final long EXPIRATION_TIME = 30; // 30 days in days
    private static final TimeUnit EXPIRATION_UNIT = TimeUnit.DAYS;

    public RedisUserRepository(RedisTemplate<String, String> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    /**
     * Save user credentials to Redis
     * Format: user:{userId} -> "email:password"
     * Also maintains reverse mapping: email_to_id:{email} -> userId
     */
    public Long saveUser(String email, String password) {
        // Check if email already exists
        String existingUserId = redisTemplate.opsForValue().get(EMAIL_ID_PREFIX + email);
        if (existingUserId != null) {
            return null; // User already exists
        }

        // Generate new user ID
        Long userId = redisTemplate.opsForValue().increment(USER_ID_COUNTER);

        // Store user credentials: user:{userId} -> "email:password"
        String userKey = USER_PREFIX + userId;
        String userValue = email + ":" + password;
        redisTemplate.opsForValue().set(userKey, userValue, EXPIRATION_TIME, EXPIRATION_UNIT);

        // Store email to ID mapping for quick lookup
        String emailKey = EMAIL_ID_PREFIX + email;
        redisTemplate.opsForValue().set(emailKey, String.valueOf(userId), EXPIRATION_TIME, EXPIRATION_UNIT);

        return userId;
    }

    /**
     * Retrieve user by email and validate password
     */
    public Long validateUser(String email, String password) {
        // Get user ID from email
        String userIdStr = redisTemplate.opsForValue().get(EMAIL_ID_PREFIX + email);
        if (userIdStr == null) {
            return null; // User not found
        }

        Long userId = Long.parseLong(userIdStr);

        // Get user credentials
        String userKey = USER_PREFIX + userId;
        String userValue = redisTemplate.opsForValue().get(userKey);
        if (userValue == null) {
            return null; // User data corrupted
        }

        // Extract and validate password
        String[] parts = userValue.split(":");
        if (parts.length < 2) {
            return null; // Invalid format
        }

        String storedPassword = parts[1];
        if (!storedPassword.equals(password)) {
            return null; // Password mismatch
        }

        return userId;
    }

    /**
     * Check if email exists
     */
    public boolean emailExists(String email) {
        Boolean exists = redisTemplate.hasKey(EMAIL_ID_PREFIX + email);
        return exists != null && exists;
    }

    /**
     * Get user by ID
     */
    public User getUserById(Long userId) {
        String userKey = USER_PREFIX + userId;
        String userValue = redisTemplate.opsForValue().get(userKey);
        if (userValue == null) {
            return null;
        }

        String[] parts = userValue.split(":");
        if (parts.length < 1) {
            return null;
        }

        String email = parts[0];
        return new User(userId, email);
    }

    /**
     * Delete user (for testing/cleanup)
     */
    public void deleteUser(String email) {
        String userIdStr = redisTemplate.opsForValue().get(EMAIL_ID_PREFIX + email);
        if (userIdStr != null) {
            Long userId = Long.parseLong(userIdStr);
            String userKey = USER_PREFIX + userId;
            redisTemplate.delete(userKey);
            redisTemplate.delete(EMAIL_ID_PREFIX + email);
        }
    }

    /**
     * Clear all users (for testing/cleanup)
     */
    public void clearAll() {
        redisTemplate.delete(redisTemplate.keys(USER_PREFIX + "*"));
        redisTemplate.delete(redisTemplate.keys(EMAIL_ID_PREFIX + "*"));
        redisTemplate.delete(USER_ID_COUNTER);
    }
}
