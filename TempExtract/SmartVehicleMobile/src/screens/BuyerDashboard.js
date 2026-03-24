import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { LogOut, RefreshCcw } from 'lucide-react-native';
import axios from 'axios';

const BuyerDashboard = ({ route, navigation }) => {
    const { user } = route.params;
    const [vehicles, setVehicles] = useState([]);
    const [loading, setLoading] = useState(true);

    const API_GET_VEHICLES = 'http://127.0.0.1:8000/api/browse-vehicles';
    const API_PURCHASE = 'http://127.0.0.1:8000/api/purchase-vehicle';

    const fetchVehicles = async () => {
        setLoading(true);
        try {
            const response = await axios.get(API_GET_VEHICLES);
            setVehicles(response.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchVehicles();
    }, []);

    const handlePurchase = (vehicle) => {
        Alert.alert(
            'Confirm Purchase',
            `Do you want to buy vehicle ${vehicle.vehicle_number} for ₹${vehicle.price}?`,
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Buy Now',
                    onPress: async () => {
                        try {
                            const res = await axios.post(API_PURCHASE, {
                                vehicle_number: vehicle.vehicle_number,
                                buyer_id: user.id,
                                buyer_name: user.name
                            });

                            if (res.data.status === 'success') {
                                Alert.alert('Success', `Purchase successful! Hash: ${res.data.transaction_id.substring(0, 20)}...`);
                                fetchVehicles();
                            }
                        } catch (error) {
                            Alert.alert('Error', 'Transaction failed');
                        }
                    }
                }
            ]
        );
    };

    const renderVehicle = ({ item }) => (
        <View style={styles.card}>
            <Image
                source={{ uri: item.picture ? `http://127.0.0.1:8000${item.picture}` : 'https://images.unsplash.com/photo-1542281286-9e0a16bb7366?auto=format&fit=crop&w=400&q=80' }}
                style={styles.cardImage}
            />
            <View style={styles.cardContent}>
                <Text style={styles.vehicleNum}>{item.vehicle_number}</Text>
                <Text style={styles.price}>₹{item.price}</Text>
                <Text style={styles.accidents}>Accidents: {item.accidents_history || 'None'}</Text>

                <TouchableOpacity
                    style={styles.buyButton}
                    onPress={() => handlePurchase(item)}
                >
                    <LinearGradient
                        colors={['#10b981', '#059669']}
                        style={styles.buyButtonGradient}
                    >
                        <Text style={styles.buyButtonText}>Buy with Blockchain</Text>
                    </LinearGradient>
                </TouchableOpacity>
            </View>
        </View>
    );

    return (
        <View style={styles.container}>
            <LinearGradient colors={['#111827', '#1f2937']} style={styles.header}>
                <View style={styles.headerRow}>
                    <View>
                        <Text style={styles.welcome}>Hello,</Text>
                        <Text style={styles.userName}>{user.name}</Text>
                    </View>
                    <TouchableOpacity onPress={() => navigation.navigate('Home')}>
                        <LogOut color="#f87171" size={24} />
                    </TouchableOpacity>
                </View>
            </LinearGradient>

            <View style={styles.sectionHeader}>
                <Text style={styles.sectionTitle}>Available Vehicles</Text>
                <TouchableOpacity onPress={fetchVehicles}>
                    <RefreshCcw color="#60a5fa" size={20} />
                </TouchableOpacity>
            </View>

            {loading ? (
                <ActivityIndicator size="large" color="#60a5fa" style={{ marginTop: 50 }} />
            ) : (
                <FlatList
                    data={vehicles}
                    renderItem={renderVehicle}
                    keyExtractor={(item) => item.vehicle_number}
                    contentContainerStyle={styles.list}
                    ListEmptyComponent={
                        <Text style={styles.emptyText}>No vehicles available at the moment.</Text>
                    }
                />
            )}
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
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 20,
    },
    sectionTitle: {
        color: '#fff',
        fontSize: 20,
        fontWeight: 'bold',
    },
    list: {
        padding: 20,
        paddingTop: 0,
    },
    card: {
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: 20,
        overflow: 'hidden',
        marginBottom: 20,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
    },
    cardImage: {
        width: '100%',
        height: 180,
    },
    cardContent: {
        padding: 15,
    },
    vehicleNum: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    price: {
        color: '#10b981',
        fontSize: 20,
        fontWeight: 'bold',
        marginVertical: 5,
    },
    accidents: {
        color: '#9ca3af',
        fontSize: 14,
        marginBottom: 15,
    },
    buyButton: {
        height: 45,
        borderRadius: 12,
        overflow: 'hidden',
    },
    buyButtonGradient: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    buyButtonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    emptyText: {
        color: '#9ca3af',
        textAlign: 'center',
        marginTop: 50,
    }
});

export default BuyerDashboard;
