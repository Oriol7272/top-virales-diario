import React, { useEffect, useState, useRef } from 'react';

// Simplified AdSense Manager to prevent 400 errors
class AdSenseManager {
  constructor() {
    this.isInitialized = false;
    this.adInstances = new Set();
    this.maxAds = 3; // Limit concurrent ads to prevent quota issues
  }

  canLoadAd() {
    return this.adInstances.size < this.maxAds;
  }

  async initializeAd(adId) {
    if (!this.canLoadAd()) {
      console.log('AdSense: Maximum ads reached, skipping');
      return false;
    }

    if (this.adInstances.has(adId)) {
      return false; // Already loaded
    }

    // AdSense re-enabled with real client ID
    console.log('AdSense: Initializing ads with real client ID');

    try {
      // Only load script once
      if (!this.isInitialized && !window.adsbygoogle) {
        const script = document.createElement('script');
        script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8755399131022250';
        script.async = true;
        script.crossOrigin = 'anonymous';
        
        script.onerror = () => {
          console.warn('AdSense: Script failed to load, ads disabled');
        };
        
        document.head.appendChild(script);
        this.isInitialized = true;
      }

      // Add with delay to prevent simultaneous requests
      setTimeout(() => {
        try {
          if (window.adsbygoogle && !this.adInstances.has(adId)) {
            this.adInstances.add(adId);
            (window.adsbygoogle = window.adsbygoogle || []).push({});
            console.log(`AdSense: Ad ${adId} initialized`);
          }
        } catch (error) {
          console.warn(`AdSense: Non-critical error for ${adId}:`, error.message);
        }
      }, this.adInstances.size * 200); // Stagger by 200ms

      return true;
    } catch (error) {
      console.warn('AdSense: Initialization failed:', error.message);
      return false;
    }
  }

  removeAd(adId) {
    this.adInstances.delete(adId);
  }
}

// Global instance
const adSenseManager = new AdSenseManager();

// Improved AdSense Component
const AdSenseAd = ({ 
  slot = 'default-slot',
  format = 'auto',
  responsive = 'true',
  style = {},
  className = '',
  adTest = true, // Set to true to prevent real ad requests during development
  disabled = false // Allow disabling ads completely
}) => {
  const [isReady, setIsReady] = useState(false);
  const adRef = useRef(null);
  const adId = useRef(`ad-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`);
  
  useEffect(() => {
    if (disabled) return;

    const initAd = async () => {
      try {
        const success = await adSenseManager.initializeAd(adId.current);
        setIsReady(success);
      } catch (error) {
        console.warn('AdSense component error:', error);
        setIsReady(false);
      }
    };

    // Delay initialization to prevent rapid requests
    const timeoutId = setTimeout(initAd, 500);

    return () => {
      clearTimeout(timeoutId);
      adSenseManager.removeAd(adId.current);
    };
  }, [disabled]);

  const defaultStyle = {
    display: 'block',
    minHeight: '250px',
    width: '100%',
    margin: '20px 0',
    backgroundColor: '#f8f9fa',
    border: '1px solid #e9ecef',
    borderRadius: '8px',
    ...style
  };

  if (disabled) {
    return (
      <div className={`ad-placeholder ${className}`} style={defaultStyle}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          color: '#6c757d',
          fontSize: '14px',
          flexDirection: 'column'
        }}>
          <div>📊 Premium Ad-Free Experience</div>
          <div style={{ fontSize: '12px', marginTop: '5px' }}>
            Upgrade to Pro to remove ads
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`adsense-container ${className}`} style={{ textAlign: 'center' }}>
      {/* AdSense Ad Unit */}
      <ins
        ref={adRef}
        className="adsbygoogle"
        style={defaultStyle}
        data-ad-client="ca-pub-8755399131022250"
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive={responsive}
        data-adtest={adTest ? 'on' : 'off'}
        key={adId.current}
      ></ins>
      
      {/* Fallback content while ads load or if they fail */}
      {!isReady && (
        <div 
          style={{
            ...defaultStyle,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#6c757d',
            fontSize: '14px',
            flexDirection: 'column'
          }}
        >
          <div>📈 Advertisement Space</div>
          <div style={{ fontSize: '12px', marginTop: '5px' }}>
            Supporting creators and content
          </div>
        </div>
      )}
    </div>
  );
};

// Optimized ad components for different tiers - TEMPORARILY DISABLED TO PREVENT 400 ERRORS
export const HeaderBannerAd = ({ userTier = "free", adTest = true }) => (
  <AdSenseAd
    slot="header-banner-728x90"
    format="auto"
    style={{ maxHeight: '90px' }}
    className="header-ad"
    adTest={adTest}
    disabled={false} // Re-enabled with real AdSense client ID
  />
);

export const SidebarRectangleAd = ({ userTier = "free", adTest = true }) => (
  <AdSenseAd
    slot="sidebar-rectangle-300x250"
    format="rectangle"
    style={{ maxWidth: '300px', height: '250px' }}
    className="sidebar-ad"
    adTest={adTest}
    disabled={false} // Re-enabled with real AdSense client ID
  />
);

export const InContentAd = ({ userTier = "free", adTest = true }) => (
  <AdSenseAd
    slot="in-content-responsive"
    format="fluid"
    style={{ minHeight: '200px' }}
    className="in-content-ad"
    adTest={adTest}
    disabled={false} // Re-enabled with real AdSense client ID
  />
);

export const MobileBannerAd = ({ userTier = "free", adTest = true }) => (
  <AdSenseAd
    slot="mobile-banner-320x100"
    format="auto"
    style={{ maxHeight: '100px' }}
    className="mobile-ad"
    adTest={adTest}
    disabled={false} // Re-enabled with real AdSense client ID
  />
);

export default AdSenseAd;