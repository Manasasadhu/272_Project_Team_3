package com.research.agent.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.research.agent.model.AuthResponse;
import com.research.agent.model.LoginRequest;
import com.research.agent.model.SignupRequest;
import com.research.agent.service.AuthService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AuthController.class)
public class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AuthService authService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testSignup() throws Exception {
        SignupRequest req = new SignupRequest();
        req.setEmail("test@example.com");
        req.setPassword("password");

        when(authService.signup(req.getEmail(), req.getPassword())).thenReturn(new AuthResponse(true, "Signup successful"));

        mockMvc.perform(post("/api/auth/signup")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated());
    }

    @Test
    public void testLogin() throws Exception {
        LoginRequest req = new LoginRequest();
        req.setEmail("test@example.com");
        req.setPassword("password");

        when(authService.login(req.getEmail(), req.getPassword())).thenReturn(new AuthResponse(true, "Login successful"));

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk());
    }

}
