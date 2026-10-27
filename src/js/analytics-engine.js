/**
 * Open Break — Client-Side Interaction & Performance Monitor (Sprint 6 / V8)
 * Measures Real User Performance, event dispatches, and Core Web Vitals telemetry in memory.
 * Completely local, zero third-party network trackers, 100% privacy-compliant.
 */
(() => {
  'use strict';

  class OpenBreakTelemetry {
    constructor() {
      this.events = [];
      this.metrics = {
        cls: 0,
        lcp: 0,
        fid: 0,
        fps: 60,
        interactionsCount: 0
      };
      this.init();
    }

    init() {
      this.measureCLS();
      this.measureLCP();
      this.measureFPS();
      this.listenInteractions();
    }

    record(category, action, label = null) {
      this.metrics.interactionsCount++;
      const record = {
        timestamp: performance.now(),
        category,
        action,
        label
      };
      this.events.push(record);
      // Keep in-memory ring buffer capped to 100 events
      if (this.events.length > 100) this.events.shift();
    }

    measureCLS() {
      if (!('PerformanceObserver' in window)) return;
      try {
        const observer = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (!entry.hadRecentInput) {
              this.metrics.cls += entry.value;
            }
          }
        });
        observer.observe({ type: 'layout-shift', buffered: true });
      } catch (e) {}
    }

    measureLCP() {
      if (!('PerformanceObserver' in window)) return;
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          if (lastEntry) {
            this.metrics.lcp = lastEntry.renderTime || lastEntry.loadTime;
          }
        });
        observer.observe({ type: 'largest-contentful-paint', buffered: true });
      } catch (e) {}
    }

    measureFPS() {
      let frames = 0;
      let lastTime = performance.now();

      const calcFPS = (now) => {
        frames++;
        if (now >= lastTime + 1000) {
          this.metrics.fps = Math.round((frames * 1000) / (now - lastTime));
          frames = 0;
          lastTime = now;
        }
        requestAnimationFrame(calcFPS);
      };
      requestAnimationFrame(calcFPS);
    }

    listenInteractions() {
      window.addEventListener('openbreak:state-changed', (e) => {
        this.record('STORE', e.detail?.action, JSON.stringify(e.detail?.payload || {}));
      });

      document.addEventListener('click', (e) => {
        const btn = e.target.closest('button, a');
        if (btn) {
          const label = btn.getAttribute('aria-label') || btn.innerText || btn.id;
          this.record('CLICK', btn.tagName, label ? label.slice(0, 30).trim() : '');
        }
      }, { passive: true });

      window.addEventListener('online', () => {
        this.record('NETWORK', 'ONLINE', 'reconnected');
      });

      window.addEventListener('offline', () => {
        this.record('NETWORK', 'OFFLINE', 'disconnected');
      });
    }

    isOnline() {
      return typeof navigator !== 'undefined' ? navigator.onLine : true;
    }

    getReport() {
      return {
        ...this.metrics,
        eventsRecorded: this.events.length,
        memoryUsage: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) + ' MB' : 'N/A'
      };
    }
  }

  if (typeof window !== 'undefined') {
    window.OpenBreakTelemetry = new OpenBreakTelemetry();
  }
})();
