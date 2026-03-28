import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import axios from 'axios';

const RegisterScreen = ({ navigation }) => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        loginid: '',
        mobile: '',
        password: '',
        role: 'buyer'
    });

    const handleRegister = async () => {
        // Basic validation
        if (!formData.name || !formData.email || !formData.loginid || !formData.mobile || !formData.password) {
            Alert.alert('Error', 'Please fill all fields');
            return;
        }

        try {
            // In a real app, this would call specialized registration endpoints
            // For now, we'll simulate success since we need to handle multi-role logic on backend
            Alert.alert('Success', 'Registration submitted! Please wait for Admin approval.', [
                { text: 'OK', onPress: () => navigation.navigate('Login') }
            ]);
        } catch (error) {
            Alert.alert('Error', 'Registration failed');
        }
    };

    return (
        <ScrollView style={styles.container}>
            <LinearGradient colors={['#111827', '#1f2937']} style={styles.background} />

            <View style={styles.content}>
                <Text style={styles.title}>Join Us</Text>
                <Text style={styles.subtitle}>Create your blockchain identity</Text>

                <View style={styles.roleContainer}>
                    {['buyer', 'seller'].map((r) => (
                        <TouchableOpacity
                            key={r}
                            style={[styles.roleButton, formData.role === r && styles.roleButtonActive]}
                            onPress={() => setFormData({ ...formData, role: r })}
                        >
                            <Text style={[styles.roleText, formData.role === r && styles.roleTextActive]}>
                                {r.toUpperCase()}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>

                <TextInput
                    style={styles.input}
                    placeholder="Full Name"
                    placeholderTextColor="#9ca3af"
                    value={formData.name}
                    onChangeText={(v) => setFormData({ ...formData, name: v })}
                />

                <TextInput
                    style={styles.input}
                    placeholder="Email Address"
                    placeholderTextColor="#9ca3af"
                    keyboardType="email-address"
                    value={formData.email}
                    onChangeText={(v) => setFormData({ ...formData, email: v })}
                />

                <TextInput
                    style={styles.input}
                    placeholder="Login ID"
                    placeholderTextColor="#9ca3af"
                    value={formData.loginid}
                    onChangeText={(v) => setFormData({ ...formData, loginid: v })}
                />

                <TextInput
                    style={styles.input}
                    placeholder="Mobile Number"
                    placeholderTextColor="#9ca3af"
                    keyboardType="phone-pad"
                    value={formData.mobile}
                    onChangeText={(v) => setFormData({ ...formData, mobile: v })}
                />

                <TextInput
                    style={styles.input}
                    placeholder="Password"
                    placeholderTextColor="#9ca3af"
                    secureTextEntry
                    value={formData.password}
                    onChangeText={(v) => setFormData({ ...formData, password: v })}
                />

                <TouchableOpacity style={styles.regButton} onPress={handleRegister}>
                    <LinearGradient colors={['#ec4899', '#be185d']} style={styles.buttonGradient}>
                        <Text style={styles.buttonText}>Register Now</Text>
                    </LinearGradient>
                </TouchableOpacity>

                <TouchableOpacity style={{ marginTop: 20, alignItems: 'center' }} onPress={() => navigation.navigate('Login')}>
                    <Text style={styles.linkText}>Already have an account? Login</Text>
                </TouchableOpacity>
            </View>
            <View style={{ height: 50 }} />
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#111827',
    },
    background: {
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        height: '100%',
    },
    content: {
        padding: 30,
        paddingTop: 80,
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
    },
    subtitle: {
        fontSize: 16,
        color: '#9ca3af',
        marginBottom: 30,
    },
    roleContainer: {
        flexDirection: 'row',
        marginBottom: 20,
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 12,
        padding: 5,
    },
    roleButton: {
        flex: 1,
        paddingVertical: 10,
        alignItems: 'center',
        borderRadius: 8,
    },
    roleButtonActive: {
        backgroundColor: 'rgba(236, 72, 153, 0.2)',
        borderWidth: 1,
        borderColor: '#ec4899',
    },
    roleText: {
        color: '#9ca3af',
        fontWeight: 'bold',
    },
    roleTextActive: {
        color: '#f472b6',
    },
    input: {
        backgroundColor: 'rgba(255,255,255,0.05)',
        height: 55,
        borderRadius: 12,
        paddingHorizontal: 20,
        color: '#fff',
        marginBottom: 15,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    regButton: {
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
    linkText: {
        color: '#9ca3af',
        fontWeight: 'bold',
    }
});

export default RegisterScreen;
