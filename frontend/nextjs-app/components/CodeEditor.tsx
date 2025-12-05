'use client';

import { useEffect, useRef } from 'react';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language?: string;
  height?: string;
}

export default function CodeEditor({ value, onChange, language = 'cpp', height = '400px' }: CodeEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [value]);

  return (
    <div className="relative">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full font-mono text-sm p-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        style={{ 
          height: height,
          minHeight: '400px',
          backgroundColor: '#1e1e1e',
          color: '#d4d4d4',
          fontFamily: 'Monaco, Menlo, "Ubuntu Mono", Consolas, monospace'
        }}
        spellCheck={false}
        placeholder={`// Write your ${language.toUpperCase()} code here`}
      />
    </div>
  );
}

