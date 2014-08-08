/** @scratch /configuration/config.js/1
 * == Configuration
 * config.js is where you will find the core Grafana configuration. This file contains parameter that
 * must be set before Grafana is run for the first time.
 */
define(['settings'],
function (Settings) {
  

  return new Settings({

    // datasources, you can add multiple
    datasources: {
      influxdb: {
        type: 'influxdb',
        url: "/influxdb/db/db",
	// url: "http://localhost:8086/db/db",
        username: 'root',
        password: 'root',
	default: true
      },
      grafana: {
        type: 'influxdb',
	url: "/influxdb/db/grafana",
        // url: "http://localhost:8086/db/grafana",
        username: 'root',
        password: 'root',
        grafanaDB: true
      },
    },

    // default start dashboard
    default_route: '/dashboard/file/default.json',

    // set to false to disable unsaved changes warning
    unsaved_changes_warning: true,

    // set the default timespan for the playlist feature
    // Example: "1m", "1h"
    playlist_timespan: "1m",

    // Add your own custom pannels
    plugins: {
      panels: []
    }

  });
});

