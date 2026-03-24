import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ImageBackground, ScrollView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Car, Shield, Cpu, Activity } from 'lucide-react-native';

const HomeScreen = ({ navigation }) => {
    return (
        <ScrollView style={styles.container}>
            <ImageBackground
                source={{ uri: 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=800&q=80' }}
                style={styles.hero}
            >
                <View style={styles.overlay}>
                    <LinearGradient
                        colors={['transparent', 'rgba(17, 24, 39, 0.9)']}
                        style={styles.gradient}
                    />
                    <View style={styles.heroContent}>
                        <Car color="#22d3ee" size={48} style={styles.icon} />
                        <Text style={styles.title}>Smart Vehicle Procurement</Text>
                        <Text style={styles.subtitle}>Transforming Vehicle Transactions with Blockchain Innovation</Text>

                        <TouchableOpacity
                            style={styles.button}
                            onPress={() => navigation.navigate('Login')}
                        >
                            <LinearGradient
                                colors={['#06b6d4', '#2563eb']}
                                style={styles.buttonGradient}
                            >
                                <Text style={styles.buttonText}>Get Started</Text>
                            </LinearGradient>
                        </TouchableOpacity>
                    </View>
                </View>
            </ImageBackground>

            <View style={styles.featuresSection}>
                <Text style={styles.sectionTitle}>Why Our System Stands Out</Text>

                <View style={styles.featureCard}>
                    <Cpu color="#67e8f9" size={32} />
                    <Text style={styles.featureTitle}>Transparent Transactions</Text>
                    <Text style={styles.featureDescription}>Leverage blockchain for secure, traceable, and tamper-proof transactions.</Text>
                </View>

                <View style={styles.featureCard}>
                    <Shield color="#4ade80" size={32} />
                    <Text style={styles.featureTitle}>Smart Contracts</Text>
                    <Text style={styles.featureDescription}>Streamline procurement with automated, error-free smart contracts.</Text>
                </View>

                <View style={styles.featureCard}>
                    <Activity color="#a78bfa" size={32} />
                    <Text style={styles.featureTitle}>Decentralized Security</Text>
                    <Text style={styles.featureDescription}>Safeguard sensitive data with decentralized storage systems.</Text>
                </View>
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
    hero: {
        height: 500,
        width: '100%',
    },
    overlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.4)',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    gradient: {
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        height: '100%',
    },
    heroContent: {
        alignItems: 'center',
        zIndex: 1,
    },
    icon: {
        marginBottom: 20,
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
        textAlign: 'center',
        marginBottom: 10,
    },
    subtitle: {
        fontSize: 18,
        color: '#d1d5db',
        textAlign: 'center',
        marginBottom: 30,
    },
    button: {
        width: 200,
        height: 50,
        borderRadius: 25,
        overflow: 'hidden',
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
    featuresSection: {
        padding: 20,
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fbbf24',
        textAlign: 'center',
        marginBottom: 30,
    },
    featureCard: {
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        padding: 20,
        borderRadius: 15,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        marginBottom: 20,
        alignItems: 'center',
    },
    featureTitle: {
        fontSize: 20,
        fontWeight: '600',
        color: '#fff',
        marginTop: 10,
        marginBottom: 5,
    },
    featureDescription: {
        fontSize: 14,
        color: '#9ca3af',
        textAlign: 'center',
    }
});

export default HomeScreen;
