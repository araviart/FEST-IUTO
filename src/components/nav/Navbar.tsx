
import "./MenuButton"
import MenuButton from './MenuButton'
import { Link } from 'react-router-dom'
import NavButton from './NavButton'
import NavLink from './NavLink'
import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import MenuConnexion from './side-menus/MenuConnexion'
import MenuPanier from './side-menus/Panier/MenuPanier'

type Props = {
  setNavInFocus : (isNavInFocus : boolean) => void;
  isTransparent : boolean,
}

export default function Navbar(props : Props) {
  const[isOpen, setIsOpen] = useState(false);
  const[menuConnexionOpen, setMenuConnexionOpen] = useState(false);
  const[menuCartOpen, setMenuCartOpen] = useState(false);
  
  useEffect(() => {
    props.setNavInFocus(menuConnexionOpen || menuCartOpen)
  }, [menuConnexionOpen, menuCartOpen])
  

  const current = window.location.pathname;

  const menuVariants = {
    closed : {
      translateY: "-100vh",
      transition:{
        duration: 0.8,
        ease: [1, -0.02, 0,1]
      },
    },
    open : {
      translateY: 0,
      transition:{
        duration: 0.8,
        ease: [1, -0.02, 0,1]
      },
    }
  }

  const navLinkVariant = (index: number) => {
    return {
      visible:{
        y:0,
        transition:{
          duration: 0.5,
          delay: 0.4 + index * 0.05,
          ease: [1, -0.02, 0,1]
        }
      },
      hidden:{
        y: "100vh",
        color:"#F3D6CB",
        transition:{
          duration: 0.5,
          delay: 0,
          ease: [1, -0.02, 0,1]
        }
      },
      hover:{
        scale: 1.5,
        transition:{
          duration: 0.3,
          ease: [1, -0.02, 0,1]
        }
      },
      visibleColor:{
        color:"#F3D6CB",
        transition:{
          duration: 0.3,
          ease: [1, -0.02, 0,1]
        }
      },
      hoverColor:{
        color:"#FFD600",
        transition:{
          duration: 0.3,
          ease: [1, -0.02, 0,1]
        }
      }
    }
  }

  return (
    <div id='Navbar' style={props.isTransparent ? {backgroundColor: "transparent"} : {backgroundColor: "#19212C"}}>
      <motion.div className="menu"
      variants={menuVariants}
      initial="closed"
      animate={isOpen ? "open" : "closed"}>
        <NavLink variants={navLinkVariant(0)} isOpen={isOpen} setIsOpen={setIsOpen} isCurrent={"/" == current} linkTo="/" name="Accueil"/>
        <NavLink variants={navLinkVariant(1)} isOpen={isOpen} setIsOpen={setIsOpen} isCurrent={"/programmation" == current} linkTo="/programmation" name="Programmation"/>
        <NavLink variants={navLinkVariant(2)} isOpen={isOpen} setIsOpen={setIsOpen} isCurrent={"/billeterie" == current} linkTo="/billeterie" name="Billeterie"/>
        <NavLink variants={navLinkVariant(3)} isOpen={isOpen} setIsOpen={setIsOpen} isCurrent={"/faq" == current} linkTo="/faq" name="FAQ"/>
      </motion.div> 
      <Link to="/" className='logo'>
        <img src="/logo.svg" alt="logo"/>
      </Link>
      <MenuConnexion isOpen={menuConnexionOpen} setIsOpen={setMenuConnexionOpen}/>
      <MenuPanier isOpen={menuCartOpen} setIsOpen={setMenuCartOpen}/>
      <div className='btns'>
        <div className="nav-btns">
          <NavButton setIsOpen={setMenuConnexionOpen} />
          <NavButton isCart setIsOpen={setMenuCartOpen} />
        </div>
        <MenuButton setIsOpen={setIsOpen} isOpen={isOpen}/>
      </div>
    </div>
  )
}
