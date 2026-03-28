import React, { useState } from 'react';
import { StyleSheet, View, ActivityIndicator, SafeAreaView, Platform, Text } from 'react-native';
import { StatusBar } from 'expo-status-bar';

// Conditionally import WebView to avoid errors on Web platform
let WebView;
if (Platform.OS !== 'web') {
  WebView = require('react-native-webview').WebView;
}

export default function App() {
  const [isLoading, setIsLoading] = useState(true);

  // Directly connect to the live Render Backend!
  const DJANGO_URL = 'https://smartvehicleprocurementsystem.onrender.com/';

  const renderContent = () => {
    if (Platform.OS === 'web') {
      // For Browser/Desktop version, we use a standard iframe
      return (
        <iframe
          src={DJANGO_URL}
          style={{ flex: 1, border: 'none', width: '100%', height: '100%' }}
          onLoad={() => setIsLoading(false)}
        />
      );
    } else {
      // For Android/iOS, we use a clean WebView framing the website
      return (
        <WebView
          source={{ uri: DJANGO_URL }}
          style={styles.webview}
          onLoadStart={() => setIsLoading(true)}
          onLoadEnd={() => setIsLoading(false)}
          javaScriptEnabled={true}
          domStorageEnabled={true}
          geolocationEnabled={true}
          scalesPageToFit={true}
          startInLoadingState={false}
          bounces={false}
          showsVerticalScrollIndicator={false}
        />
      );
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="dark" />

      <View style={{ flex: 1 }}>
        {renderContent()}

        {isLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#10b981" />
            <Text style={styles.loadingText}>Starting Smart Vehicle...</Text>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingTop: Platform.OS === 'android' ? 35 : 0,
  },
  webview: {
    flex: 1,
  },
  loadingContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#333',
  },
  footer: {
    height: 30,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  footerText: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
  }
});
