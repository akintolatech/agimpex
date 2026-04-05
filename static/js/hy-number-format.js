(function (global) {
  'use strict';

  function formatHyNumber(value) {
    const num = Number(value);
    if (!isFinite(num)) return '';
    const negative = num < 0;
    const abs = Math.abs(num);
    const cents = Math.round(abs * 100);
    let intPart = Math.floor(cents / 100);
    const frac = cents % 100;
    let intStr = String(intPart).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    if (frac === 0) {
      return (negative ? '-' : '') + intStr;
    }
    let fracStr = String(frac).padStart(2, '0').replace(/0+$/, '');
    return (negative ? '-' : '') + intStr + '.' + fracStr;
  }

  function parseHyNumber(text) {
    if (text === null || text === undefined) return 0;
    const cleaned = String(text).replace(/,/g, '').replace(/\s/g, '').trim();
    const n = parseFloat(cleaned);
    return isFinite(n) ? n : 0;
  }

  global.formatHyNumber = formatHyNumber;
  global.parseHyNumber = parseHyNumber;
})(typeof window !== 'undefined' ? window : globalThis);
