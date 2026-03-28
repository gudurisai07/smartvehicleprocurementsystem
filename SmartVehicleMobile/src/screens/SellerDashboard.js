import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { LogOut, PlusCircle, History } from 'lucide-react-native';

const SellerDashboard = ({ route, navigation }) => {
    const { user } = route.params;

    return (
        <View style={styles.container}>
            <LinearGradient colors={['#111827', '#1f2937']} style={styles.header}>
                <View style={styles.headerRow}>
                    <View>
                        <Text style={styles.welcome}>Seller Panel,</Text>
                        <Text style={styles.userName}>{user.name}</Text>
                    </View>
                    <TouchableOpacity onPress={() => navigation.navigate('Home')}>
                        <LogOut color="#f87171" size={24} />
                    </TouchableOpacity>
                </View>
            </LinearGradient>

            <View style={styles.content}>
                <TouchableOpacity style={styles.menuItem}>
                    <PlusCircle color="#10b981" size={32} />
                    <View style={styles.menuTextContainer}>
                        <Text style={styles.menuTitle}>Add New Vehicle</Text>
                        <Text style={styles.menuSub}>Register a new vehicle on blockchain</Text>
                    </View>
                </TouchableOpacity>

                <TouchableOpacity style={styles.menuItem}>
                    <History color="#60a5fa" size={32} />
                    <View style={styles.menuTextContainer}>
                        <Text style={styles.menuTitle}>Vehicle History</Text>
                        <Text style={styles.menuSub}>Check your registered vehicles status</Text>
                    </View>
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#111827',
    },
    header: {
        paddingTop: 60,
        paddingBottom: 25,
        paddingHorizontal: 20,
        borderBottomLeftRadius: 30,
        borderBottomRightRadius: 30,
    },
    headerRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    welcome: {
        color: '#9ca3af',
        fontSize: 16,
    },
    userName: {
        color: '#fff',
        fontSize: 24,
        fontWeight: 'bold',
    },
    content: {
        padding: 20,
        marginTop: 20,
    },
    menuItem: {
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        flexDirection: 'row',
        alignItems: 'center',
        padding: 20,
        borderRadius: 20,
        marginBottom: 20,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
    },
    menuTextContainer: {
        marginLeft: 20,
    },
    menuTitle: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    menuSub: {
        color: '#9ca3af',
        fontSize: 14,
    }
});

export default SellerDashboard;
