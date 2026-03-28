import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import axios from 'axios';

const LoginScreen = ({ navigation }) => {
    const [loginid, setLoginid] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('buyer'); // buyer, seller, admin
    const [loading, setLoading] = useState(false);

    // Use your local IP address for physical device testing
    const API_URL = 'http://127.0.0.1:8000/api/login';

    const handleLogin = async () => {
        if (!loginid || !password) {
            Alert.alert('Error', 'Please enter all fields');
            return;
        }

        setLoading(true);
        try {
            const response = await axios.post(API_URL, {
                loginid,
                password,
                role
            });

            if (response.data) {
                const user = response.data;
                if (role === 'buyer') navigation.navigate('BuyerDashboard', { user });
                else if (role === 'seller') navigation.navigate('SellerDashboard', { user });
                else if (role === 'admin') navigation.navigate('AdminDashboard', { user });
            }
        } catch (error) {
            Alert.alert('Login Failed', error.response?.data?.error || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            <LinearGradient
                colors={['#111827', '#1f2937']}
                style={styles.background}
            />

            <View style={styles.content}>
                <Text style={styles.title}>Welcome Back</Text>
                <Text style={styles.subtitle}>Login to your account</Text>

                <View style={styles.roleContainer}>
                    {['buyer', 'seller', 'admin'].map((r) => (
                        <TouchableOpacity
                            key={r}
                            style={[styles.roleButton, role === r && styles.roleButtonActive]}
                            onPress={() => setRole(r)}
                        >
                            <Text style={[styles.roleText, role === r && styles.roleTextActive]}>
                                {r.toUpperCase()}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>

                <TextInput
                    style={styles.input}
                    placeholder="Login ID"
                    placeholderTextColor="#9ca3af"
                    value={loginid}
                    onChangeText={setLoginid}
                    autoCapitalize="none"
                />

                <TextInput
                    style={styles.input}
                    placeholder="Password"
                    placeholderTextColor="#9ca3af"
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry
                />

                <TouchableOpacity
                    style={styles.loginButton}
                    onPress={handleLogin}
                    disabled={loading}
                >
                    <LinearGradient
                        colors={['#8b5cf6', '#6d28d9']}
                        style={styles.buttonGradient}
                    >
                        {loading ? (
                            <ActivityIndicator color="#fff" />
                        ) : (
                            <Text style={styles.buttonText}>Login</Text>
                        )}
                    </LinearGradient>
                </TouchableOpacity>

                <View style={styles.footer}>
                    <Text style={styles.footerText}>Don't have an account? </Text>
                    <TouchableOpacity onPress={() => navigation.navigate('Register')}>
                        <Text style={styles.linkText}>Register</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    background: {
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        height: '100%',
    },
    content: {
        flex: 1,
        padding: 30,
        justifyContent: 'center',
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 5,
    },
    subtitle: {
        fontSize: 16,
        color: '#9ca3af',
        marginBottom: 40,
    },
    roleContainer: {
        flexDirection: 'row',
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 12,
        padding: 5,
        marginBottom: 30,
    },
    roleButton: {
        flex: 1,
        paddingVertical: 10,
        alignItems: 'center',
        borderRadius: 8,
    },
    roleButtonActive: {
        backgroundColor: 'rgba(139, 92, 246, 0.2)',
        borderWidth: 1,
        borderColor: '#8b5cf6',
    },
    roleText: {
        color: '#9ca3af',
        fontSize: 12,
        fontWeight: 'bold',
    },
    roleTextActive: {
        color: '#a78bfa',
    },
    input: {
        backgroundColor: 'rgba(255,255,255,0.05)',
        height: 55,
        borderRadius: 12,
        paddingHorizontal: 20,
        color: '#fff',
        marginBottom: 20,
        fontSize: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    loginButton: {
        height: 55,
        borderRadius: 12,
        overflow: 'hidden',
        marginTop: 10,
    },
    buttonGradient: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    footer: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginTop: 30,
    },
    footerText: {
        color: '#9ca3af',
    },
    linkText: {
        color: '#8b5cf6',
        fontWeight: 'bold',
    }
});

export default LoginScreen;
