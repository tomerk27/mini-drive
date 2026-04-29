/**
 * @file CyberDriveMark.jsx
 * SVG logo mark for CyberDrive: an indigo rounded square containing a cloud
 * outline with a shield inside and a small amber security dot as an accent.
 */

/**
 * Renders the CyberDrive SVG logo mark at a configurable size.
 *
 * @param {object} props
 * @param {number} [props.size=40] - Width and height of the SVG in pixels.
 * @returns {JSX.Element} An inline SVG element scaled to the requested size.
 */
const CyberDriveMark = ({ size = 40 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 64 64"
    aria-label="Cyber Drive"
    style={{ display: 'block', flexShrink: 0 }}
  >
    {/* Indigo rounded-square plate */}
    <rect x="2" y="2" width="60" height="60" rx="15" fill="#6366f1" />

    {/* Cloud — single outlined stroke */}
    <path
      d="M20 42
         Q12 42 12 34
         Q12 27.5 18 26
         Q19.5 19 26 17
         Q34 14.5 39 19
         Q43 22.5 43 27
         Q50 27 51.5 33
         Q53 40 47 42
         Z"
      fill="none"
      stroke="#ffffff"
      strokeWidth="2.4"
      strokeLinejoin="round"
      strokeLinecap="round"
    />

    {/* Shield — floats inside cloud without touching its stroke */}
    <path
      d="M32 27.5
         L36.5 29.5
         L36.5 33.5
         Q36.5 37 32 38.5
         Q27.5 37 27.5 33.5
         L27.5 29.5
         Z"
      fill="none"
      stroke="#ffffff"
      strokeWidth="2.2"
      strokeLinejoin="round"
      strokeLinecap="round"
    />

    {/* Amber security dot — single accent */}
    <circle cx="32" cy="33.5" r="1.6" fill="#fbbf24" />
  </svg>
);

export default CyberDriveMark;
