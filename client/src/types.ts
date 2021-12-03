/* eslint camelcase: "off" */

interface User {
  id: number,
  username: string,
  email: string,
  is_superuser: boolean
}

interface Frame {
  id: string,
  name: string,
}

interface ScanDecision {
  id: string,
  creator: User,
  created: string,
  decision: string,
  note: string,
  user_identified_artifacts: Object,
}

interface Scan {
  id: string,
  name: string,
  scan_id: string,
  scan_type: string,
  experiment: string,
  decisions: ScanDecision[],
  frames: Frame[],
}

interface Experiment {
  id: string,
  name: string,
  lock_owner: {
    id: number,
    username: string,
  },
  scans?: Scan[],
  project: string,
  note: string,
}

interface ProjectSettings {
  importPath: string,
  exportPath: string,
  permissions: Object,
}

interface Project {
  id: string,
  name: string,
  experiments?: Experiment[],
  settings: ProjectSettings,
}

interface Settings {
  importPath: string,
  exportPath: string,
  globalImportExport: boolean
}

export {
  User, Project, Settings, ScanDecision,
};
