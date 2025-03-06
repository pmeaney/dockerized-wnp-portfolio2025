"use client"
import React, { useState, useEffect } from 'react';
import PortfolioItem from './PortfolioItem';

export default function PortfolioGrid() {
  const [portfolioItems, setPortfolioItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Function to fetch portfolio items from the Wagtail API
    const fetchPortfolioItems = async () => {
      try {
        setLoading(true);
        // Using the custom portfolio API endpoint we created
        const response = await fetch('/api/v2/portfolio/');
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Transform the data if necessary to match the component props
        const items = data.items ? data.items.map(item => ({
          id: item.id,
          title: item.title,
          subtitle: item.meta?.subtitle || null,
          thumbnail: item.thumbnail,
          tags: item.tags || [],
          main_button_left_text: item.main_button_left_text || 'Preview',
          main_button_left_url: item.main_button_left_url || '#',
          secondary_button_right_text: item.secondary_button_right_text || 'Source Code',
          secondary_button_right_url: item.secondary_button_right_url || '#'
        })) : [];
        
        setPortfolioItems(items);
      } catch (err) {
        console.error("Error fetching portfolio items:", err);
        setError(err.message);
        
        // For development - fallback to sample data when API isn't available
        setPortfolioItems(samplePortfolioItems);
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolioItems();
  }, []);

  if (loading) {
    return (
      <section className="section" id="portfolio">
        <div className="container has-text-centered">
          <progress className="progress is-primary" max="100">Loading</progress>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="section" id="portfolio">
        <div className="container">
          <div className="notification is-danger">
            <p>Error loading portfolio items: {error}</p>
            <p>Please try again later or contact the administrator.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="section" id="portfolio">
      <div className="container">
        <h1 className="title has-text-centered">Portfolio</h1>
        <div className="card-grid">
          {portfolioItems.map(item => (
            <PortfolioItem key={item.id} item={item} />
          ))}
        </div>
      </div>
    </section>
  );
}

// Sample data for development and testing
const samplePortfolioItems = [
  {
    id: 1,
    title: 'Admin',
    subtitle: 'Light',
    thumbnail: '../images/admin.png',
    tags: [
      { name: 'v0.7.2', style: 'is-default', url: 'https://github.com/jgthms/bulma/releases/tag/0.7.2' },
      { name: 'Desktop', style: 'is-default' },
      { name: 'WIP', style: 'is-danger' }
    ],
    main_button_left_text: 'Preview',
    main_button_left_url: 'templates/admin.html',
    secondary_button_right_text: 'Source Code',
    secondary_button_right_url: 'https://github.com/BulmaTemplates/bulma-templates/blob/master/templates/admin.html'
  },
  {
    id: 2,
    title: 'Dashboard',
    subtitle: 'Dark',
    thumbnail: '../images/admin.png',
    tags: [
      { name: 'v0.9.1', style: 'is-default' },
      { name: 'Mobile', style: 'is-info' },
      { name: 'Responsive', style: 'is-success' }
    ],
    main_button_left_text: 'Preview',
    main_button_left_url: 'templates/dashboard.html',
    secondary_button_right_text: 'Source Code',
    secondary_button_right_url: 'https://github.com/BulmaTemplates/bulma-templates/blob/master/templates/dashboard.html'
  },
  {
    id: 3,
    title: 'E-commerce',
    subtitle: 'Shop',
    thumbnail: '../images/admin.png',
    tags: [
      { name: 'v1.0.0', style: 'is-default' },
      { name: 'Responsive', style: 'is-success' }
    ],
    main_button_left_text: 'Preview',
    main_button_left_url: 'templates/shop.html',
    secondary_button_right_text: 'Source Code',
    secondary_button_right_url: 'https://github.com/BulmaTemplates/bulma-templates/blob/master/templates/shop.html'
  }
];