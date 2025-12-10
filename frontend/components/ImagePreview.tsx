'use client';

import React from 'react';
import { ImageInfo } from '@/types';

interface ImagePreviewProps {
  images: File[] | ImageInfo[];
  onRemove?: (index: number) => void;
  isUploaded?: boolean;
}

const ImagePreview: React.FC<ImagePreviewProps> = ({ images, onRemove, isUploaded = false }) => {
  const getImageSrc = (image: File | ImageInfo, index: number): string => {
    if (image instanceof File) {
      return URL.createObjectURL(image);
    } else {
      // ImageInfo from API
      return `http://localhost:8000/${image.file_path}`;
    }
  };

  const getImageName = (image: File | ImageInfo): string => {
    if (image instanceof File) {
      return image.name;
    } else {
      return image.file_name;
    }
  };

  if (images.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 mt-2">
      {images.map((image, index) => (
        <div key={index} className="relative group">
          <img
            src={getImageSrc(image, index)}
            alt={getImageName(image)}
            className="w-20 h-20 object-cover rounded-lg border-2 border-accent-cyan/30 hover:border-accent-cyan transition-all"
          />
          {onRemove && (
            <button
              onClick={() => onRemove(index)}
              className="absolute -top-2 -right-2 bg-accent-pink hover:bg-accent-pink/80 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-glow-purple"
              type="button"
            >
              ×
            </button>
          )}
          <div className="absolute bottom-0 left-0 right-0 bg-black/70 text-xs text-text-secondary p-1 rounded-b-lg truncate opacity-0 group-hover:opacity-100 transition-opacity">
            {getImageName(image)}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImagePreview;
