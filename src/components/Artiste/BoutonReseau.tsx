import { motion } from 'framer-motion';
import {useState} from 'react'

type Props = {
    href : string;
    type: "soundcloud" | "spotify" | "instagram" | "twitter" | "youtube";
}

export default function BoutonReseau(props: Props) {
  const [isHovered, setIsHovered] = useState(false)

  const btnVariants = {
    default:{
        backgroundColor:"#E45A3B00",
        transition:{
            duration: 0.3,
            ease:"easeOut",
        }
    },
    hover:{
        backgroundColor:"#E45A3B",
        transition:{
            duration: 0.3,
            ease:"easeOut",
        }
    }
  }

  const svgVariants = {
    default:{
        fill:"#E45A3B",
        transition:{
            duration:0.3,
            ease: [1, 0, 0,1]
        }
    },
    hover:{
        fill:"#FFFBEE",
        transition:{
            duration:0.3,
            ease: [1, 0, 0,1]
        }
    }
  }

  return (
    <motion.a href={props.href} className='btn-reseau'
    onMouseEnter={() => setIsHovered(true)}
    onMouseLeave={() => setIsHovered(false)}
    variants={btnVariants}
    initial="default"
    animate={isHovered ? "hover" : "default"}
    >

        {
            props.type === "soundcloud" ? (
                <svg width="51" height="22" viewBox="0 0 51 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <motion.path d="M24.0742 3.20787V21.779H44.0157C48.2271 21.4821 50.1166 18.878 50.1166 15.68C50.1166 12.2993 47.567 9.581 44.1523 9.581C43.2873 9.581 42.5588 9.76374 41.8076 10.0835C41.2612 4.73833 36.7312 0.558105 31.1539 0.558105C28.4905 0.558105 25.9637 1.56319 24.0742 3.20787ZM22.071 5.53783C21.388 5.12666 20.6596 4.80686 19.8628 4.64696V21.779H23.0271V4.28148C22.6856 4.64696 22.3669 5.10382 22.071 5.53783ZM16.7214 4.30432V21.779H18.8157V4.37285C18.3832 4.30432 17.9506 4.28148 17.4954 4.28148C17.2222 4.28148 16.9718 4.28148 16.7214 4.30432ZM12.5555 5.7891V21.779H14.6271V4.73833C13.8758 4.9896 13.1701 5.35509 12.5555 5.7891ZM8.75387 11.4998C8.61729 11.4998 8.4807 11.3627 8.32135 11.2942V21.779H10.4157V7.75358C9.57339 8.85003 9.00428 10.1521 8.75387 11.4998ZM4.10996 10.8602V21.5735C4.58801 21.7105 5.13435 21.779 5.72622 21.779H6.22704V10.6775C6.04492 10.6546 5.86281 10.6318 5.72622 10.6318C5.13435 10.6318 4.58801 10.7231 4.10996 10.8602ZM0.0351562 16.2054C0.0351562 17.9186 0.809142 19.4262 2.01565 20.4542V11.9795C0.809142 12.9846 0.0351562 14.515 0.0351562 16.2054Z"
                    variants={svgVariants}
                    initial="default"
                    animate={isHovered ? "hover" : "default"}
                    />
                </svg>
            )
            : props.type === "spotify" ? (
                <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <motion.path d="M31.8 17.8C25.4 14 14.7 13.6 8.6 15.5C7.6 15.8 6.6 15.2 6.3 14.3C6 13.3 6.6 12.3 7.5 12C14.6 9.9 26.3 10.3 33.7 14.7C34.6 15.2 34.9 16.4 34.4 17.3C33.9 18 32.7 18.3 31.8 17.8ZM31.6 23.4C31.1 24.1 30.2 24.4 29.5 23.9C24.1 20.6 15.9 19.6 9.6 21.6C8.8 21.8 7.9 21.4 7.7 20.6C7.5 19.8 7.9 18.9 8.7 18.7C16 16.5 25 17.6 31.2 21.4C31.8 21.7 32.1 22.7 31.6 23.4ZM29.2 28.9C28.8 29.5 28.1 29.7 27.5 29.3C22.8 26.4 16.9 25.8 9.9 27.4C9.2 27.6 8.6 27.1 8.4 26.5C8.2 25.8 8.7 25.2 9.3 25C16.9 23.3 23.5 24 28.7 27.2C29.4 27.5 29.5 28.3 29.2 28.9ZM20 0C17.3736 0 14.7728 0.517315 12.3463 1.52241C9.91982 2.5275 7.71504 4.00069 5.85786 5.85786C2.10714 9.60859 0 14.6957 0 20C0 25.3043 2.10714 30.3914 5.85786 34.1421C7.71504 35.9993 9.91982 37.4725 12.3463 38.4776C14.7728 39.4827 17.3736 40 20 40C25.3043 40 30.3914 37.8929 34.1421 34.1421C37.8929 30.3914 40 25.3043 40 20C40 17.3736 39.4827 14.7728 38.4776 12.3463C37.4725 9.91982 35.9993 7.71504 34.1421 5.85786C32.285 4.00069 30.0802 2.5275 27.6537 1.52241C25.2272 0.517315 22.6264 0 20 0Z"
                    variants={svgVariants}
                    initial="default"
                    animate={isHovered ? "hover" : "default"}
                    />
                </svg>
            )
            : props.type === "instagram" ? (
                <svg width="45" height="45" viewBox="0 0 45 45" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <motion.path d="M13.0353 0H31.9141C39.106 0 44.9494 5.84342 44.9494 13.0353V31.9141C44.9494 35.3712 43.576 38.6868 41.1314 41.1314C38.6868 43.576 35.3712 44.9494 31.9141 44.9494H13.0353C5.84342 44.9494 0 39.106 0 31.9141V13.0353C0 9.57814 1.37336 6.26255 3.81796 3.81796C6.26255 1.37336 9.57814 0 13.0353 0ZM12.5858 4.49494C10.44 4.49494 8.38204 5.34737 6.8647 6.8647C5.34737 8.38204 4.49494 10.44 4.49494 12.5858V32.3635C4.49494 36.836 8.11336 40.4544 12.5858 40.4544H32.3635C34.5094 40.4544 36.5673 39.602 38.0847 38.0847C39.602 36.5673 40.4544 34.5094 40.4544 32.3635V12.5858C40.4544 8.11336 36.836 4.49494 32.3635 4.49494H12.5858ZM34.2739 7.86614C35.019 7.86614 35.7335 8.16212 36.2604 8.68898C36.7873 9.21583 37.0832 9.93039 37.0832 10.6755C37.0832 11.4206 36.7873 12.1351 36.2604 12.662C35.7335 13.1888 35.019 13.4848 34.2739 13.4848C33.5288 13.4848 32.8142 13.1888 32.2874 12.662C31.7605 12.1351 31.4646 11.4206 31.4646 10.6755C31.4646 9.93039 31.7605 9.21583 32.2874 8.68898C32.8142 8.16212 33.5288 7.86614 34.2739 7.86614ZM22.4747 11.2373C25.455 11.2373 28.3133 12.4213 30.4207 14.5287C32.5281 16.6361 33.712 19.4944 33.712 22.4747C33.712 25.455 32.5281 28.3133 30.4207 30.4207C28.3133 32.5281 25.455 33.712 22.4747 33.712C19.4944 33.712 16.6361 32.5281 14.5287 30.4207C12.4213 28.3133 11.2373 25.455 11.2373 22.4747C11.2373 19.4944 12.4213 16.6361 14.5287 14.5287C16.6361 12.4213 19.4944 11.2373 22.4747 11.2373ZM22.4747 15.7323C20.6865 15.7323 18.9715 16.4426 17.7071 17.7071C16.4426 18.9715 15.7323 20.6865 15.7323 22.4747C15.7323 24.2629 16.4426 25.9778 17.7071 27.2423C18.9715 28.5067 20.6865 29.2171 22.4747 29.2171C24.2629 29.2171 25.9778 28.5067 27.2423 27.2423C28.5067 25.9778 29.2171 24.2629 29.2171 22.4747C29.2171 20.6865 28.5067 18.9715 27.2423 17.7071C25.9778 16.4426 24.2629 15.7323 22.4747 15.7323Z"
                    variants={svgVariants}
                    initial="default"
                    animate={isHovered ? "hover" : "default"}
                    />
                </svg>
            )
            : props.type === "twitter" ? (
                <svg width="49" height="39" viewBox="0 0 49 39" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <motion.path d="M49 4.58824C47.1965 5.39118 45.2524 5.91882 43.238 6.17118C45.2992 4.95529 46.892 3.02824 47.6415 0.711176C45.6974 1.85824 43.5425 2.66118 41.2706 3.12C39.4202 1.14706 36.8203 0 33.869 0C28.3647 0 23.8676 4.40471 23.8676 9.84176C23.8676 10.6218 23.9613 11.3788 24.1252 12.09C15.7868 11.6771 8.36185 7.75412 3.41969 1.81235C2.55306 3.25765 2.06119 4.95529 2.06119 6.74471C2.06119 10.1629 3.81788 13.1912 6.53489 14.9118C4.87189 14.9118 3.326 14.4529 1.9675 13.7647V13.8335C1.9675 18.6053 5.43403 22.5971 10.0249 23.4918C8.55094 23.8868 7.00357 23.9418 5.5043 23.6524C6.14047 25.608 7.38639 27.3193 9.06691 28.5455C10.7474 29.7718 12.7781 30.4514 14.8733 30.4888C11.3216 33.2428 6.91902 34.7314 2.3891 34.71C1.59273 34.71 0.796367 34.6641 0 34.5724C4.45029 37.3712 9.74379 39 15.412 39C33.869 39 44.011 23.9965 44.011 10.9888C44.011 10.5529 44.011 10.14 43.9876 9.70412C45.9551 8.32765 47.6415 6.58412 49 4.58824Z" 
                    variants={svgVariants}
                    initial="default"
                    animate={isHovered ? "hover" : "default"}
                    />
                </svg>
            )
            : (
                <svg width="53" height="37" viewBox="0 0 53 37" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <motion.path d="M52.9878 13.04C53.1069 9.6163 52.3532 6.21826 50.7969 3.16135C49.741 1.90703 48.2755 1.06056 46.6559 0.769439C39.9569 0.165541 33.2301 -0.0819771 26.5045 0.0279454C19.8034 -0.0869662 13.1009 0.152565 6.42537 0.74552C5.10558 0.984034 3.88422 1.59906 2.91031 2.51554C0.743496 4.50083 0.502739 7.89735 0.261982 10.7676C-0.0873274 15.9284 -0.0873274 21.1065 0.261982 26.2673C0.331634 27.8828 0.573748 29.4864 0.984253 31.0511C1.27455 32.2592 1.86187 33.3769 2.69363 34.3041C3.67416 35.2691 4.92397 35.9191 6.28091 36.1698C11.4714 36.8063 16.7014 37.0701 21.9301 36.9591C30.3566 37.0787 37.7479 36.9591 46.4873 36.2894C47.8776 36.0541 49.1626 35.4033 50.1709 34.4237C50.845 33.7537 51.3484 32.9338 51.6396 32.0318C52.5006 29.4069 52.9235 26.6598 52.8915 23.8993C52.9878 22.5598 52.9878 14.4751 52.9878 13.04ZM21.0634 25.3344V10.5285L35.3162 17.9673C31.3197 20.1679 26.0471 22.6555 21.0634 25.3344Z"
                    variants={svgVariants}
                    initial="default"
                    animate={isHovered ? "hover" : "default"}
                    />
                </svg>
            )
        }
    </motion.a>
  )
}
