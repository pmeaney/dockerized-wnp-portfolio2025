import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

const PortfolioItem = ({ item }) => {
  return (
    <div className="card card-item">
      <header className="card-header">
        <p className="card-header-title">
          <span>
            {item.title} {item.subtitle && <small>({item.subtitle})</small>}
          </span>
          <span className="is-pulled-right">
            {item.tags && item.tags.map((tag, index) => (
              <span key={index} className={`tag ${tag.style || 'is-default'}`}>
                {tag.url ? (
                  <a href={tag.url}>{tag.name}</a>
                ) : (
                  tag.name
                )}
              </span>
            ))}
          </span>
        </p>
      </header>
      <div className="card-content">
        <figure className="image">
          {item.thumbnail && (
            <img
              src={item.thumbnail}
              alt={`${item.title} screenshot`}
            />
          )}
        </figure>
      </div>
      <footer className="card-footer">
        {item.main_button_left_text && (
          <a href={item.main_button_left_url} className="card-footer-item">
            {item.main_button_left_text}
          </a>
        )}
        {item.secondary_button_right_text && (
          <a href={item.secondary_button_right_url} className="card-footer-item">
            {item.secondary_button_right_text}
          </a>
        )}
      </footer>
    </div>
  );
};

export default PortfolioItem;